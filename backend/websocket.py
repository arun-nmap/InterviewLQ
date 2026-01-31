import json
from fastapi import WebSocketDisconnect

from ai.interviewer import get_question
from ai.whisper_stream import transcribe_audio
from ai.evaluator import evaluate_answer
from ai.emotion_camera import detect_emotion
from ai.confidence import fuse_confidence   # ✅ FIXED IMPORT
from ai.difficulty import adjust_difficulty
from ai.tips import generate_tip
from utils.timeline import add_point
from ai.report_pdf import generate_pdf


async def interview_socket(ws):
    await ws.accept()

    history = []
    timeline = []
    difficulty = "medium"

    try:
        for i in range(4):
            # --------------------
            # Send question
            # --------------------
            question = get_question(i, difficulty)
            await ws.send_json({
                "question": question,
                "difficulty": difficulty
            })

            # --------------------
            # Receive audio / stop
            # --------------------
            raw = await ws.receive_text()
            data = json.loads(raw)

            # Stop interview safely
            if data.get("type") == "stop":
                generate_pdf(history, timeline)
                await ws.send_json({"end": True})
                await ws.close()
                return

            # --------------------
            # Transcription (SAFE FALLBACK)
            # --------------------
            try:
                answer = transcribe_audio(data.get("audio", ""))
                if not answer or not answer.strip():
                    answer = "[Voice transcription disabled – fallback mode]"
            except Exception:
                answer = "[Voice transcription disabled – fallback mode]"

            # --------------------
            # Emotion (NORMALIZED)
            # --------------------
            raw_emotion = detect_emotion()
            emotion = raw_emotion.lower() if raw_emotion else "neutral"

            # --------------------
            # Evaluation
            # --------------------
            relevance = evaluate_answer(answer)
            confidence = fuse_confidence(relevance, emotion)

            # Difficulty adapts correctly
            difficulty = adjust_difficulty(confidence)

            tip = generate_tip(confidence, emotion)
            timeline = add_point(timeline, confidence, emotion)

            history.append({
                "question": question,
                "answer": answer,
                "confidence": confidence,
                "emotion": emotion,
                "difficulty": difficulty
            })

            # --------------------
            # Send realtime update
            # --------------------
            await ws.send_json({
                "confidence": confidence,
                "emotion": emotion,
                "difficulty": difficulty,
                "tip": tip,
                "transcript": answer,
                "radar": {
                    "Communication": int(relevance),
                    "Confidence": int(confidence),
                    "Leadership": 60,
                    "Sociability": 65,
                    "Professionalism": 70
                }
            })

        # --------------------
        # Normal interview end
        # --------------------
        generate_pdf(history, timeline)
        await ws.send_json({"end": True})
        await ws.close()

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        print("WebSocket error:", e)
        try:
            await ws.close()
        except:
            pass
