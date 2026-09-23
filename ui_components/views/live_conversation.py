"""
SignBridge AI — Intelligent Two-Way Live Conversation View
User Hand Action (Camera, Hands-Only) → Natural Conversational AI → 3D Avatar Reaction
Powered by MediaPipe Hands, Natural Response Engine, and AvatarReactionController.
"""

import json
import streamlit as st
import streamlit.components.v1 as components

from response_engine import (
    ConversationContext,
    ConversationTurn,
    ContextualResponse,
    generate_natural_response,
)
from ui_components.styles import render_html


def render_live_conversation_view():
    """Renders the User Action -> AI Understanding -> Avatar Reaction interface."""

    # Top Status & Controls Header
    c_hdr, c_rst = st.columns([2.0, 0.8], gap="medium")
    with c_hdr:
        render_html(
            """
            <div style="margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 0.78rem; font-weight: 700; color: #5B5CEB; text-transform: uppercase; letter-spacing: 0.06em;">Natural Live Interaction</span>
                    <span style="color: #CBD5E1;">•</span>
                    <span style="font-size: 0.78rem; color: #64748B;">Hands-Only Input ➔ Natural AI Conversation ➔ 3D Human Avatar</span>
                </div>
            </div>
            """
        )
    with c_rst:
        if st.button("🗑️ Reset Conversation Memory", key="btn_reset_live_conv", type="secondary", use_container_width=True):
            st.session_state["conv_memory_reset"] = True
            st.rerun()

    # Interactive Two-Way Component (HTML5 + WebRTC + MediaPipe Hands + Natural Response Engine + Speech)
    component_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SignBridge Natural Live Communication</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
        
        <!-- MediaPipe CDN (Hands Only) -->
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js" crossorigin="anonymous"></script>

        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                user-select: none;
            }}

            body {{
                font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
                background-color: transparent;
                color: #0F172A;
                padding: 4px;
            }}

            .live-comm-grid {{
                display: grid;
                grid-template-columns: 1fr 1.25fr;
                gap: 20px;
                width: 100%;
                margin-bottom: 14px;
            }}

            @media (max-width: 960px) {{
                .live-comm-grid {{
                    grid-template-columns: 1fr;
                }}
            }}

            /* User Action Card */
            .comm-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 18px;
                padding: 16px;
                box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
                display: flex;
                flex-direction: column;
                gap: 12px;
                position: relative;
            }}

            .comm-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                flex-wrap: wrap;
                gap: 8px;
            }}

            .comm-title {{
                font-size: 0.95rem;
                font-weight: 700;
                color: #0F172A;
                display: flex;
                align-items: center;
                gap: 8px;
            }}

            .badge {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 0.76rem;
                font-weight: 600;
            }}

            .badge-listening {{
                background: rgba(91, 92, 235, 0.10);
                color: #5B5CEB;
                border: 1px solid rgba(91, 92, 235, 0.25);
            }}

            .badge-ready {{
                background: rgba(16, 185, 129, 0.10);
                color: #059669;
                border: 1px solid rgba(16, 185, 129, 0.25);
            }}

            .badge-responding {{
                background: rgba(245, 158, 11, 0.12);
                color: #D97706;
                border: 1px solid rgba(245, 158, 11, 0.30);
            }}

            /* Camera Container */
            .video-wrap {{
                position: relative;
                width: 100%;
                height: 280px;
                border-radius: 14px;
                overflow: hidden;
                background: #0F172A;
                border: 1px solid #CBD5E1;
            }}

            #webcam {{
                width: 100%;
                height: 100%;
                object-fit: cover;
                transform: scaleX(-1);
            }}

            #output_canvas {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transform: scaleX(-1);
                pointer-events: none;
            }}

            .cam-hud {{
                position: absolute;
                top: 10px;
                left: 10px;
                display: flex;
                gap: 6px;
                z-index: 10;
            }}

            .hud-pill {{
                background: rgba(15, 23, 42, 0.75);
                backdrop-filter: blur(8px);
                color: #FFFFFF;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 600;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }}

            /* Recognition Bar */
            .recognition-bar {{
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 10px 14px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }}

            .user-sign-text {{
                font-size: 1.10rem;
                font-weight: 800;
                color: #0F172A;
            }}

            .intent-tag {{
                background: rgba(91, 92, 235, 0.10);
                color: #5B5CEB;
                padding: 3px 8px;
                border-radius: 6px;
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.03em;
            }}

            /* Avatar Reaction Viewport */
            .avatar-viewport {{
                position: relative;
                width: 100%;
                height: 280px;
                border-radius: 14px;
                overflow: hidden;
                background: #F1F5F9;
                border: 1px solid #CBD5E1;
            }}

            #avatar_frame {{
                width: 100%;
                height: 100%;
                border: none;
            }}

            /* Floating Speech Bubble */
            .speech-bubble {{
                position: absolute;
                top: 14px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(12px);
                border: 1.5px solid #5B5CEB;
                border-radius: 999px;
                padding: 7px 18px;
                color: #0F172A;
                font-weight: 700;
                font-size: 0.88rem;
                box-shadow: 0 4px 18px rgba(91, 92, 235, 0.20);
                z-index: 20;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
                max-width: 90%;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }}

            .speech-bubble.hidden {{
                opacity: 0;
                transform: translate(-50%, -10px) scale(0.95);
                pointer-events: none;
            }}

            /* Avatar Status Bar */
            .avatar-status-bar {{
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 10px 14px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 8px;
            }}

            /* Recent Conversation Timeline */
            .timeline-card {{
                background: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 14px;
                padding: 14px 16px;
                margin-bottom: 14px;
                box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
            }}

            .timeline-header {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin-bottom: 10px;
            }}

            .timeline-title {{
                font-size: 0.80rem;
                font-weight: 700;
                color: #64748B;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}

            .turns-container {{
                display: flex;
                flex-direction: column;
                gap: 8px;
                max-height: 170px;
                overflow-y: auto;
            }}

            .turn-row {{
                display: flex;
                align-items: flex-start;
                gap: 10px;
                font-size: 0.84rem;
                padding: 6px 10px;
                border-radius: 8px;
            }}

            .turn-user {{
                background: #F8FAFC;
                border-left: 3px solid #5B5CEB;
            }}

            .turn-assistant {{
                background: #F0FDF4;
                border-left: 3px solid #10B981;
            }}

            .turn-speaker {{
                font-weight: 700;
                min-width: 85px;
            }}

            .turn-user .turn-speaker {{
                color: #5B5CEB;
            }}

            .turn-assistant .turn-speaker {{
                color: #059669;
            }}

            .turn-content {{
                color: #0F172A;
                font-weight: 500;
                flex: 1;
            }}

            .turn-meta {{
                font-size: 0.70rem;
                color: #94A3B8;
                font-weight: 600;
            }}

            /* Action Buttons & Scenario Chips */
            .btn-row {{
                display: flex;
                gap: 8px;
                flex-wrap: wrap;
            }}

            .action-btn {{
                background: #FFFFFF;
                border: 1px solid #CBD5E1;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 0.78rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.15s ease;
                display: inline-flex;
                align-items: center;
                gap: 6px;
            }}

            .action-btn:hover {{
                background: rgba(91, 92, 235, 0.08);
                border-color: #5B5CEB;
                color: #5B5CEB;
            }}

            .scenario-chip {{
                background: #F1F5F9;
                border: 1px solid #E2E8F0;
                border-radius: 999px;
                padding: 5px 12px;
                font-size: 0.76rem;
                font-weight: 600;
                color: #334155;
                cursor: pointer;
                transition: all 0.15s ease;
            }}

            .scenario-chip:hover {{
                background: rgba(91, 92, 235, 0.12);
                border-color: #5B5CEB;
                color: #5B5CEB;
            }}

            /* Debug Panel */
            .debug-container {{
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 12px;
                padding: 12px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.74rem;
                color: #475569;
            }}

            .debug-grid {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 8px;
                margin-top: 6px;
            }}

            @media (max-width: 768px) {{
                .debug-grid {{
                    grid-template-columns: repeat(2, 1fr);
                }}
            }}

            .debug-item {{
                background: #FFFFFF;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 6px 8px;
            }}

            .debug-label {{
                color: #64748B;
                font-size: 0.68rem;
                text-transform: uppercase;
                margin-bottom: 2px;
            }}

            .debug-val {{
                color: #0F172A;
                font-weight: 700;
            }}
        </style>
    </head>
    <body>

        <!-- Two-Way Live Communication Grid -->
        <div class="live-comm-grid">
            
            <!-- USER ACTION PANEL (CAMERA - HANDS ONLY) -->
            <div class="comm-card">
                <div class="comm-header">
                    <div class="comm-title">
                        <span>📷</span>
                        <span>User Action (Hands Only)</span>
                    </div>
                    <span id="comm_state_badge" class="badge badge-listening">● Listening</span>
                </div>

                <div class="video-wrap">
                    <video id="webcam" playsinline muted autoplay></video>
                    <canvas id="output_canvas"></canvas>
                    <div class="cam-hud">
                        <div class="hud-pill" id="hands_count_hud">Hands: 0</div>
                        <div class="hud-pill" id="tracking_state_hud">Tracking: Active (Hands Only)</div>
                    </div>
                </div>

                <!-- Recognition Result Bar -->
                <div class="recognition-bar">
                    <div>
                        <div style="font-size: 0.70rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Recognized Sign</div>
                        <div class="user-sign-text" id="user_sign_display">WAITING FOR GESTURE...</div>
                    </div>
                    <div style="text-align: right;">
                        <span class="intent-tag" id="intent_tag_display">AWAITING HANDS</span>
                        <div style="font-size: 0.72rem; color: #64748B; margin-top: 3px;" id="conf_display">Confidence: 0%</div>
                    </div>
                </div>
            </div>

            <!-- SIGNBRIDGE AVATAR REACTION PANEL -->
            <div class="comm-card">
                <div class="comm-header">
                    <div class="comm-title">
                        <span>👤</span>
                        <span>SignBridge Human Avatar Reaction</span>
                    </div>
                    <span id="avatar_state_badge" class="badge badge-ready">● Ready</span>
                </div>

                <div class="avatar-viewport">
                    <!-- Floating Speech Bubble Overlay -->
                    <div class="speech-bubble hidden" id="avatar_speech_bubble">
                        <span id="bubble_icon">💬</span>
                        <span id="bubble_text">Hello! What's up?</span>
                    </div>

                    <!-- 3D Human Avatar Iframe -->
                    <iframe id="avatar_frame" src="https://ai-avatar-jade-zeta.vercel.app/?text=HELLO&speed=0.10&pause=800&emotion=friendly&intensity=50"></iframe>
                </div>

                <!-- Avatar Status & Dynamic Response Bar -->
                <div class="avatar-status-bar">
                    <div style="flex: 1;">
                        <div style="font-size: 0.70rem; color: #64748B; font-weight: 600; text-transform: uppercase;">Avatar Response</div>
                        <div style="font-size: 0.92rem; font-weight: 800; color: #0F172A;" id="avatar_reaction_display">Ready — Listening for hand gestures</div>
                    </div>
                    <div style="display: flex; gap: 6px;">
                        <button class="action-btn" id="btn_manual_speak">🔊 Speak</button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Compact Recent Conversation Timeline (Max 5 Turns) -->
        <div class="timeline-card">
            <div class="timeline-header">
                <span class="timeline-title">💬 Recent Conversation Context (Active Memory)</span>
                <span style="font-size: 0.72rem; color: #64748B;" id="active_topic_badge">Topic: General</span>
            </div>
            <div class="turns-container" id="turns_container">
                <div class="turn-row turn-assistant">
                    <span class="turn-speaker">SignBridge</span>
                    <span class="turn-content">Hello! I'm watching your hands. Perform a sign anytime.</span>
                    <span class="turn-meta">Init</span>
                </div>
            </div>
        </div>

        <!-- Contextual Demo Scenarios -->
        <div style="margin-bottom: 12px;">
            <div style="font-size: 0.74rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                ⚡ Natural Conversational Scenarios (Test Dynamic Flows)
            </div>
            <div class="btn-row">
                <button class="scenario-chip" onclick="runScenario('HI_GREETING')">👋 Scenario: Greeting (Hi ➔ "Hello! What's up?")</button>
                <button class="scenario-chip" onclick="runScenario('HELP_HOSPITAL_YES')">🏥 Scenario: Help ➔ Hospital ➔ Yes ("Okay. I can help with that.")</button>
                <button class="scenario-chip" onclick="runScenario('WATER_OFFER')">💧 Scenario: Water Offer (Water ➔ Yes)</button>
                <button class="scenario-chip" onclick="runScenario('GRATITUDE')">🤝 Scenario: Gratitude (Thank You ➔ "You're welcome!")</button>
                <button class="scenario-chip" onclick="runScenario('HOW_ARE_YOU')">😊 Scenario: How Are You ("I'm doing well! How are you?")</button>
                <button class="scenario-chip" onclick="runScenario('STANDALONE_YES')">❓ Scenario: Standalone YES ("Got it. How can I help?")</button>
            </div>
        </div>

        <!-- Quick Individual Sign Triggers -->
        <div style="margin-bottom: 14px;">
            <div style="font-size: 0.74rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 6px;">
                🤟 Test Individual Hand Signs
            </div>
            <div class="btn-row">
                <button class="action-btn" onclick="simulateUserSign('HI')">👋 HI</button>
                <button class="action-btn" onclick="simulateUserSign('HELLO')">👋 HELLO</button>
                <button class="action-btn" onclick="simulateUserSign('HELP')">🆘 HELP</button>
                <button class="action-btn" onclick="simulateUserSign('HOSPITAL')">🏥 HOSPITAL</button>
                <button class="action-btn" onclick="simulateUserSign('YES')">👍 YES</button>
                <button class="action-btn" onclick="simulateUserSign('NO')">👎 NO</button>
                <button class="action-btn" onclick="simulateUserSign('WATER')">💧 WATER</button>
                <button class="action-btn" onclick="simulateUserSign('FOOD')">🍲 FOOD</button>
                <button class="action-btn" onclick="simulateUserSign('DOCTOR')">🩺 DOCTOR</button>
                <button class="action-btn" onclick="simulateUserSign('WHERE')">📍 WHERE</button>
                <button class="action-btn" onclick="simulateUserSign('WHAT')">❓ WHAT</button>
                <button class="action-btn" onclick="simulateUserSign('THANK_YOU')">🤝 THANK YOU</button>
                <button class="action-btn" onclick="simulateUserSign('EMERGENCY')">🚨 EMERGENCY</button>
            </div>
        </div>

        <!-- Developer Real-Time Pipeline Monitor -->
        <div class="debug-container">
            <div style="font-weight: 700; color: #0F172A; margin-bottom: 4px;">DEVELOPER CONVERSATIONAL PIPELINE MONITOR</div>
            <div class="debug-grid">
                <div class="debug-item">
                    <div class="debug-label">Recognized Sign</div>
                    <div class="debug-val" id="dbg_action">IDLE</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Pending Question</div>
                    <div class="debug-val" id="dbg_pending">NONE</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Active Topic</div>
                    <div class="debug-val" id="dbg_topic">GENERAL</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Interpreted Intent</div>
                    <div class="debug-val" id="dbg_intent">WAITING</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Natural Response</div>
                    <div class="debug-val" id="dbg_response">-</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Avatar Sign (Gloss)</div>
                    <div class="debug-val" id="dbg_gloss">-</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Avatar State</div>
                    <div class="debug-val" id="dbg_state">READY</div>
                </div>
                <div class="debug-item">
                    <div class="debug-label">Tracking Mode</div>
                    <div class="debug-val" style="color: #10B981;" id="dbg_tracking">HANDS ONLY (21 pts)</div>
                </div>
            </div>
        </div>

        <script>
            // =========================================================================
            // CONVERSATION MEMORY & STATE
            // =========================================================================
            const conversationContext = {{
                recentTurns: [],
                currentTopic: null,
                currentIntent: null,
                pendingQuestion: null,
                pendingExpectedResponses: [],
                greetingCount: 0
            }};

            // DOM Elements
            const videoElement = document.getElementById('webcam');
            const canvasElement = document.getElementById('output_canvas');
            const canvasCtx = canvasElement.getContext('2d');
            const handsCountHud = document.getElementById('hands_count_hud');
            const userSignDisplay = document.getElementById('user_sign_display');
            const intentTagDisplay = document.getElementById('intent_tag_display');
            const confDisplay = document.getElementById('conf_display');
            const avatarFrame = document.getElementById('avatar_frame');
            const avatarReactionDisplay = document.getElementById('avatar_reaction_display');
            const avatarSpeechBubble = document.getElementById('avatar_speech_bubble');
            const bubbleText = document.getElementById('bubble_text');
            const commStateBadge = document.getElementById('comm_state_badge');
            const avatarStateBadge = document.getElementById('avatar_state_badge');
            const turnsContainer = document.getElementById('turns_container');
            const activeTopicBadge = document.getElementById('active_topic_badge');

            // Debug Elements
            const dbgAction = document.getElementById('dbg_action');
            const dbgPending = document.getElementById('dbg_pending');
            const dbgTopic = document.getElementById('dbg_topic');
            const dbgIntent = document.getElementById('dbg_intent');
            const dbgResponse = document.getElementById('dbg_response');
            const dbgGloss = document.getElementById('dbg_gloss');
            const dbgState = document.getElementById('dbg_state');

            function updateTimelineUI() {{
                turnsContainer.innerHTML = '';
                conversationContext.recentTurns.slice(-5).forEach(turn => {{
                    const row = document.createElement('div');
                    row.className = `turn-row turn-${{turn.speaker}}`;
                    
                    const spk = document.createElement('span');
                    spk.className = 'turn-speaker';
                    spk.textContent = turn.speaker === 'user' ? 'You (Sign)' : 'SignBridge';
                    
                    const content = document.createElement('span');
                    content.className = 'turn-content';
                    content.textContent = turn.sign ? `🤟 ${{turn.sign}} — "${{turn.text}}"` : turn.text;
                    
                    const meta = document.createElement('span');
                    meta.className = 'turn-meta';
                    meta.textContent = turn.intent || '';
                    
                    row.appendChild(spk);
                    row.appendChild(content);
                    row.appendChild(meta);
                    turnsContainer.appendChild(row);
                }});
                turnsContainer.scrollTop = turnsContainer.scrollHeight;
                activeTopicBadge.textContent = `Topic: ${{conversationContext.currentTopic || 'General'}} | Pending: ${{conversationContext.pendingQuestion || 'None'}}`;
            }}

            function addConversationTurn(speaker, text, sign = null, intent = null, confidence = 0.94) {{
                const turn = {{
                    id: 'turn_' + Date.now(),
                    speaker: speaker,
                    inputType: sign ? 'sign' : 'text',
                    text: text,
                    sign: sign,
                    intent: intent,
                    confidence: confidence,
                    timestamp: Date.now()
                }};
                conversationContext.recentTurns.push(turn);
                if (conversationContext.recentTurns.length > 10) {{
                    conversationContext.recentTurns.shift();
                }}
                updateTimelineUI();
            }}

            // =========================================================================
            // NATURAL RESPONSE ENGINE
            // =========================================================================
            function generateNaturalResponse(recognizedSign, conversationContext, confidence = 0.94) {{
                const sign = recognizedSign.toUpperCase().trim().replace(/ /g, '_');
                const pending = conversationContext.pendingQuestion;
                const topic = conversationContext.currentTopic;

                // Low confidence fallback
                if (confidence < 0.70) {{
                    return {{
                        responseText: "Sorry, I wasn't sure what that sign meant. Please try again.",
                        intent: "UNCERTAIN",
                        confidence: confidence,
                        responseGloss: [],
                        avatarExpression: "concerned"
                    }};
                }}

                // --- 1. GREETINGS (HI / HELLO / HEY / GOOD MORNING) ---
                if (sign === "HELLO" || sign === "HI" || sign === "HEY") {{
                    if (conversationContext.greetingCount > 0) {{
                        return {{
                            responseText: "Hi again! What's on your mind?",
                            intent: "GREETING",
                            confidence: confidence,
                            responseGloss: ["HELLO"],
                            avatarExpression: "friendly"
                        }};
                    }} else {{
                        conversationContext.greetingCount++;
                        return {{
                            responseText: "Hello! What's up?",
                            intent: "GREETING",
                            confidence: confidence,
                            responseGloss: ["HELLO"],
                            avatarExpression: "friendly"
                        }};
                    }}
                }}

                if (sign === "GOOD_MORNING" || sign === "MORNING") {{
                    return {{
                        responseText: "Good morning! How are you?",
                        intent: "GREETING",
                        confidence: confidence,
                        responseGloss: ["GOOD", "DAY"],
                        avatarExpression: "friendly",
                        newPending: "HOW_ARE_YOU"
                    }};
                }}

                if (sign === "GOOD_EVENING" || sign === "EVENING") {{
                    return {{
                        responseText: "Good evening! How's it going?",
                        intent: "GREETING",
                        confidence: confidence,
                        responseGloss: ["GOOD", "NIGHT"],
                        avatarExpression: "friendly",
                        newPending: "HOW_ARE_YOU"
                    }};
                }}

                // --- 2. CASUAL CONVERSATION (HOW ARE YOU) ---
                if (sign === "HOW_ARE_YOU" || (sign === "HOW" && pending === "HOW_ARE_YOU")) {{
                    return {{
                        responseText: "I'm doing well! How are you?",
                        intent: "CASUAL_CONVERSATION",
                        confidence: confidence,
                        responseGloss: ["GOOD", "HOW"],
                        avatarExpression: "friendly"
                    }};
                }}

                // --- 3. GRATITUDE (THANK YOU) ---
                if (sign === "THANK_YOU" || sign === "THANKYOU" || sign === "THANKS") {{
                    const variations = ["You're welcome!", "Anytime! Happy to help.", "You're very welcome!"];
                    const chosen = variations[Math.floor(Math.random() * variations.length)];
                    return {{
                        responseText: chosen,
                        intent: "GRATITUDE",
                        confidence: confidence,
                        responseGloss: ["WELCOME"],
                        avatarExpression: "warm",
                        clearPending: true
                    }};
                }}

                // --- 4. REQUEST FOR HELP (HELP) ---
                if (sign === "HELP") {{
                    return {{
                        responseText: "Of course! What do you need help with?",
                        intent: "REQUEST_HELP",
                        confidence: confidence,
                        responseGloss: ["HELP", "HOW"],
                        avatarExpression: "attentive",
                        newPending: "WHAT_HELP_NEEDED",
                        newTopic: "HELP"
                    }};
                }}

                // --- 5. HOSPITAL ---
                if (sign === "HOSPITAL") {{
                    if (topic === "HELP" || pending === "WHAT_HELP_NEEDED") {{
                        return {{
                            responseText: "Are you looking for the hospital?",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["HOSPITAL"],
                            avatarExpression: "attentive",
                            newPending: "HOSPITAL_LOCATION",
                            newTopic: "HOSPITAL"
                        }};
                    }} else {{
                        return {{
                            responseText: "The hospital is located nearby. Stay calm, I'm here to help.",
                            intent: "REQUEST_LOCATION",
                            confidence: confidence,
                            responseGloss: ["HOSPITAL"],
                            avatarExpression: "attentive",
                            newTopic: "HOSPITAL"
                        }};
                    }}
                }}

                // --- 6. DOCTOR ---
                if (sign === "DOCTOR") {{
                    if (topic === "HELP" || topic === "EMERGENCY" || pending === "WHAT_HELP_NEEDED") {{
                        return {{
                            responseText: "Do you need a doctor right away?",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["DOCTOR", "HELP"],
                            avatarExpression: "serious",
                            newPending: "DOCTOR_NEEDED",
                            newTopic: "DOCTOR"
                        }};
                    }} else {{
                        return {{
                            responseText: "Do you need medical attention or a doctor?",
                            intent: "REQUEST",
                            confidence: confidence,
                            responseGloss: ["DOCTOR"],
                            avatarExpression: "serious",
                            newPending: "DOCTOR_NEEDED",
                            newTopic: "DOCTOR"
                        }};
                    }}
                }}

                // --- 7. YES (Context-Aware Confirmation) ---
                if (sign === "YES") {{
                    if (pending === "HOSPITAL_LOCATION" || topic === "HOSPITAL") {{
                        return {{
                            responseText: "Okay. I can help with that.",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["GOOD", "HELP"],
                            avatarExpression: "attentive",
                            newTopic: "HOSPITAL",
                            clearPending: true
                        }};
                    }} else if (pending === "OFFER_WATER" || topic === "WATER") {{
                        return {{
                            responseText: "Sure, I'll get you some.",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["WATER"],
                            avatarExpression: "friendly",
                            newTopic: "WATER",
                            clearPending: true
                        }};
                    }} else if (pending === "OFFER_FOOD" || topic === "FOOD") {{
                        return {{
                            responseText: "Sure, I'll arrange some food for you.",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["FOOD"],
                            avatarExpression: "friendly",
                            newTopic: "FOOD",
                            clearPending: true
                        }};
                    }} else if (pending === "NEED_HELP" || pending === "WHAT_HELP_NEEDED" || topic === "HELP") {{
                        return {{
                            responseText: "Of course! What do you need help with?",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["HELP", "HOW"],
                            avatarExpression: "attentive",
                            newPending: "WHAT_HELP_NEEDED",
                            newTopic: "HELP"
                        }};
                    }} else if (pending === "READY_TO_CONTINUE" || topic === "CONTINUE") {{
                        return {{
                            responseText: "Great, let's continue.",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "friendly",
                            clearPending: true
                        }};
                    }} else if (pending === "DOCTOR_NEEDED" || topic === "DOCTOR" || topic === "EMERGENCY") {{
                        return {{
                            responseText: "Understood. I will contact medical assistance for you.",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["DOCTOR", "HELP"],
                            avatarExpression: "serious",
                            newTopic: "MEDICAL",
                            clearPending: true
                        }};
                    }} else {{
                        // Standalone YES
                        return {{
                            responseText: "Got it. How can I help?",
                            intent: "CONFIRMATION",
                            confidence: confidence,
                            responseGloss: ["HOW", "HELP"],
                            avatarExpression: "friendly",
                            newPending: "WHAT_HELP_NEEDED",
                            newTopic: "HELP"
                        }};
                    }}
                }}

                // --- 8. NO (Context-Aware Denial) ---
                if (sign === "NO") {{
                    if (pending === "OFFER_WATER" || topic === "WATER") {{
                        return {{
                            responseText: "No problem.",
                            intent: "DENIAL",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "friendly",
                            clearPending: true
                        }};
                    }} else if (pending === "OFFER_FOOD" || topic === "FOOD") {{
                        return {{
                            responseText: "No problem. Let me know if you get hungry later.",
                            intent: "DENIAL",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "friendly",
                            clearPending: true
                        }};
                    }} else if (pending === "NEED_HELP" || pending === "WHAT_HELP_NEEDED" || topic === "HELP") {{
                        return {{
                            responseText: "No problem. Let me know if you need anything.",
                            intent: "DENIAL",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "warm",
                            clearPending: true
                        }};
                    }} else if (pending === "READY_TO_CONTINUE") {{
                        return {{
                            responseText: "Take your time. Let me know when you are ready.",
                            intent: "DENIAL",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "warm",
                            clearPending: true
                        }};
                    }} else {{
                        return {{
                            responseText: "Understood. Let me know if you need anything.",
                            intent: "DENIAL",
                            confidence: confidence,
                            responseGloss: ["GOOD"],
                            avatarExpression: "neutral",
                            clearPending: true
                        }};
                    }}
                }}

                // --- 9. WHAT (Context-Aware Question) ---
                if (sign === "WHAT" || sign === "QUESTION") {{
                    if (topic === "HOSPITAL") {{
                        return {{
                            responseText: "The hospital provides emergency medical care. Do you need directions?",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["HOSPITAL"],
                            avatarExpression: "attentive"
                        }};
                    }} else if (topic === "WATER") {{
                        return {{
                            responseText: "I can get you clean drinking water.",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["WATER"],
                            avatarExpression: "friendly"
                        }};
                    }} else {{
                        return {{
                            responseText: "What would you like to know? I'm here to assist.",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["QUESTION"],
                            avatarExpression: "attentive"
                        }};
                    }}
                }}

                // --- 10. WHERE (Context-Aware Location Question) ---
                if (sign === "WHERE") {{
                    if (topic === "HOSPITAL") {{
                        return {{
                            responseText: "Yes, I can help you find the hospital. It's straight ahead.",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["HOSPITAL"],
                            avatarExpression: "attentive",
                            newTopic: "HOSPITAL"
                        }};
                    }} else if (topic === "DOCTOR" || topic === "MEDICAL") {{
                        return {{
                            responseText: "The medical clinic is straight down this corridor.",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["DOCTOR"],
                            avatarExpression: "attentive",
                            newTopic: "DOCTOR"
                        }};
                    }} else {{
                        return {{
                            responseText: "Where would you like to go? I can give you directions.",
                            intent: "QUESTION",
                            confidence: confidence,
                            responseGloss: ["QUESTION"],
                            avatarExpression: "attentive",
                            newPending: "ASK_LOCATION",
                            newTopic: "LOCATION"
                        }};
                    }}
                }}

                // --- 11. WATER & FOOD (Requests) ---
                if (sign === "WATER") {{
                    return {{
                        responseText: "Would you like some water?",
                        intent: "REQUEST",
                        confidence: confidence,
                        responseGloss: ["WATER"],
                        avatarExpression: "attentive",
                        newPending: "OFFER_WATER",
                        newTopic: "WATER"
                    }};
                }}

                if (sign === "FOOD") {{
                    return {{
                        responseText: "Would you like some food or something to eat?",
                        intent: "REQUEST",
                        confidence: confidence,
                        responseGloss: ["FOOD"],
                        avatarExpression: "friendly",
                        newPending: "OFFER_FOOD",
                        newTopic: "FOOD"
                    }};
                }}

                // --- 12. EMERGENCY ---
                if (sign === "EMERGENCY") {{
                    return {{
                        responseText: "Emergency assistance is on alert. What happened?",
                        intent: "EMERGENCY",
                        confidence: confidence,
                        responseGloss: ["HELP"],
                        avatarExpression: "serious",
                        newPending: "DOCTOR_NEEDED",
                        newTopic: "EMERGENCY"
                    }};
                }}

                // --- 13. GOOD / BAD / PLEASE / SORRY / STOP / HOW ---
                if (sign === "GOOD") {{
                    return {{
                        responseText: "Glad to hear that!",
                        intent: "CASUAL_CONVERSATION",
                        confidence: confidence,
                        responseGloss: ["GOOD"],
                        avatarExpression: "friendly"
                    }};
                }}

                if (sign === "BAD") {{
                    return {{
                        responseText: "I'm sorry to hear that. How can I make it better?",
                        intent: "CASUAL_CONVERSATION",
                        confidence: confidence,
                        responseGloss: ["HELP"],
                        avatarExpression: "concerned",
                        newPending: "WHAT_HELP_NEEDED",
                        newTopic: "HELP"
                    }};
                }}

                if (sign === "PLEASE") {{
                    return {{
                        responseText: "Certainly! Whatever you need.",
                        intent: "REQUEST",
                        confidence: confidence,
                        responseGloss: ["GOOD"],
                        avatarExpression: "friendly"
                    }};
                }}

                if (sign === "SORRY") {{
                    return {{
                        responseText: "No worries at all! Everything is okay.",
                        intent: "CASUAL_CONVERSATION",
                        confidence: confidence,
                        responseGloss: ["GOOD"],
                        avatarExpression: "warm"
                    }};
                }}

                if (sign === "STOP") {{
                    return {{
                        responseText: "Stopping now. Standing by.",
                        intent: "REQUEST",
                        confidence: confidence,
                        responseGloss: ["STOP"],
                        avatarExpression: "neutral"
                    }};
                }}

                if (sign === "HOW") {{
                    return {{
                        responseText: "I can explain how. What would you like to learn?",
                        intent: "QUESTION",
                        confidence: confidence,
                        responseGloss: ["HOW"],
                        avatarExpression: "attentive"
                    }};
                }}

                // Fallback
                return {{
                    responseText: `Got it. You signed ${{sign}}. How can I help?`,
                    intent: "CASUAL_CONVERSATION",
                    confidence: confidence,
                    responseGloss: ["GOOD"],
                    avatarExpression: "friendly"
                }};
            }}

            // =========================================================================
            // AVATAR REACTION CONTROLLER & STATE MACHINE
            // =========================================================================
            class AvatarReactionController {{
                constructor() {{
                    this.state = "READY";
                    this.lastTriggeredSign = null;
                    this.cooldownUntil = 0;
                    this.responseTimeout = null;
                    this.currentResponse = null;
                }}

                setState(newState) {{
                    this.state = newState;
                    dbgState.textContent = newState;
                    if (newState === "READY") {{
                        commStateBadge.className = "badge badge-listening";
                        commStateBadge.textContent = "● Listening";
                        avatarStateBadge.className = "badge badge-ready";
                        avatarStateBadge.textContent = "✓ Ready";
                    }} else if (newState === "LISTENING") {{
                        commStateBadge.className = "badge badge-listening";
                        commStateBadge.textContent = "● Hands Detected";
                        avatarStateBadge.className = "badge badge-listening";
                        avatarStateBadge.textContent = "● Attentive";
                    }} else if (newState === "UNDERSTANDING" || newState === "THINKING") {{
                        commStateBadge.className = "badge badge-responding";
                        commStateBadge.textContent = "● Understanding...";
                        avatarStateBadge.className = "badge badge-responding";
                        avatarStateBadge.textContent = "● Processing";
                    }} else if (newState === "RESPONDING" || newState === "SIGNING") {{
                        commStateBadge.className = "badge badge-ready";
                        commStateBadge.textContent = "✓ Recognized";
                        avatarStateBadge.className = "badge badge-responding";
                        avatarStateBadge.textContent = "● Responding";
                    }}
                }}

                reactToAction(recognizedSign, confidence) {{
                    const now = Date.now();
                    // Hold Cooldown: do not spam while user holds the same sign
                    if (now < this.cooldownUntil && this.lastTriggeredSign === recognizedSign) {{
                        return;
                    }}

                    this.setState("UNDERSTANDING");
                    this.lastTriggeredSign = recognizedSign;
                    this.cooldownUntil = now + 2500;

                    // 1. Generate Natural Conversational Response
                    const response = generateNaturalResponse(recognizedSign, conversationContext, confidence);
                    this.currentResponse = response;

                    // 2. Update Conversation Memory
                    addConversationTurn('user', recognizedSign, recognizedSign, response.intent, confidence);

                    if (response.newPending) {{
                        conversationContext.pendingQuestion = response.newPending;
                    }} else if (response.clearPending) {{
                        conversationContext.pendingQuestion = null;
                    }}

                    if (response.newTopic) {{
                        conversationContext.currentTopic = response.newTopic;
                    }}

                    addConversationTurn('assistant', response.responseText, null, response.intent);

                    // 3. Update Telemetry & UI
                    dbgAction.textContent = recognizedSign;
                    dbgPending.textContent = conversationContext.pendingQuestion || "NONE";
                    dbgTopic.textContent = conversationContext.currentTopic || "GENERAL";
                    dbgIntent.textContent = response.intent;
                    dbgResponse.textContent = response.responseText;
                    dbgGloss.textContent = (response.responseGloss || []).join(" ") || "-";

                    userSignDisplay.textContent = `🤟 ${{recognizedSign}}`;
                    intentTagDisplay.textContent = response.intent;
                    confDisplay.textContent = `Confidence: ${{Math.round(confidence * 100)}}%`;

                    avatarReactionDisplay.textContent = `Response: "${{response.responseText}}"`;

                    // 4. Update Avatar 3D Frame with Genuine Supported ISL Gloss & Expression
                    const glossList = (response.responseGloss && response.responseGloss.length > 0) ? response.responseGloss : ["HELLO"];
                    const glossText = encodeURIComponent(glossList.join(" "));
                    const emotion = encodeURIComponent(response.avatarExpression || "friendly");
                    avatarFrame.src = `https://ai-avatar-jade-zeta.vercel.app/?text=${{glossText}}&speed=0.10&pause=800&emotion=${{emotion}}&intensity=60`;

                    // 5. Speech Bubble & Voice
                    this.showSpeechBubble(response.responseText);
                    this.speakResponse(response.responseText);

                    this.setState("RESPONDING");

                    // 6. Reset to Ready after speech / animation duration
                    if (this.responseTimeout) clearTimeout(this.responseTimeout);
                    this.responseTimeout = setTimeout(() => {{
                        this.returnToReady();
                    }}, Math.max(3200, (glossList.length * 1200)));
                }}

                showSpeechBubble(text) {{
                    bubbleText.textContent = text;
                    avatarSpeechBubble.classList.remove('hidden');
                }}

                hideSpeechBubble() {{
                    avatarSpeechBubble.classList.add('hidden');
                }}

                speakResponse(text) {{
                    if ('speechSynthesis' in window) {{
                        window.speechSynthesis.cancel();
                        const utterance = new SpeechSynthesisUtterance(text);
                        utterance.rate = 1.0;
                        utterance.pitch = 1.05;
                        window.speechSynthesis.speak(utterance);
                    }}
                }}

                returnToReady() {{
                    this.hideSpeechBubble();
                    this.setState("READY");
                }}
            }}

            const reactionController = new AvatarReactionController();

            // Manual speech replay button
            document.getElementById('btn_manual_speak').addEventListener('click', () => {{
                if (reactionController.currentResponse) {{
                    reactionController.speakResponse(reactionController.currentResponse.responseText);
                }} else {{
                    reactionController.speakResponse("Hello! What's up?");
                }}
            }});

            // Simulate user gesture
            window.simulateUserSign = function(sign) {{
                reactionController.reactToAction(sign, 0.95);
            }};

            // Run Interactive Contextual Scenarios
            window.runScenario = function(scenarioKey) {{
                if (scenarioKey === 'HI_GREETING') {{
                    reactionController.reactToAction('HI', 0.96);
                }} else if (scenarioKey === 'HELP_HOSPITAL_YES') {{
                    // Turn 1: User signs HI
                    reactionController.reactToAction('HI', 0.96);
                    // Turn 2: User signs HELP
                    setTimeout(() => {{
                        reactionController.reactToAction('HELP', 0.94);
                    }}, 3500);
                    // Turn 3: User signs HOSPITAL
                    setTimeout(() => {{
                        reactionController.reactToAction('HOSPITAL', 0.95);
                    }}, 7200);
                    // Turn 4: User signs YES
                    setTimeout(() => {{
                        reactionController.reactToAction('YES', 0.96);
                    }}, 10800);
                }} else if (scenarioKey === 'WATER_OFFER') {{
                    reactionController.reactToAction('WATER', 0.94);
                    setTimeout(() => {{
                        reactionController.reactToAction('YES', 0.95);
                    }}, 3500);
                }} else if (scenarioKey === 'GRATITUDE') {{
                    reactionController.reactToAction('THANK_YOU', 0.96);
                }} else if (scenarioKey === 'HOW_ARE_YOU') {{
                    reactionController.reactToAction('HOW_ARE_YOU', 0.95);
                }} else if (scenarioKey === 'STANDALONE_YES') {{
                    conversationContext.pendingQuestion = null;
                    conversationContext.currentTopic = null;
                    reactionController.reactToAction('YES', 0.94);
                }}
            }};

            // =========================================================================
            // GEOMETRIC HAND RECOGNITION (HANDS ONLY - ZERO FACE/BODY TRACKING)
            // =========================================================================
            function dist(p1, p2) {{
                return Math.hypot(p1.x - p2.x, p1.y - p2.y);
            }}

            function isFingerExtended(lm, tipIdx, pipIdx) {{
                const wrist = lm[0];
                return dist(lm[tipIdx], wrist) > dist(lm[pipIdx], wrist) * 1.20;
            }}

            function isThumbExtended(lm) {{
                return dist(lm[4], lm[0]) > dist(lm[2], lm[0]) * 1.15;
            }}

            // Rolling temporal buffer for stable recognition
            let frameBuffer = [];

            function classifyHandAction(multiHandLandmarks) {{
                if (!multiHandLandmarks || multiHandLandmarks.length === 0) return null;

                const h1 = multiHandLandmarks[0];
                const h2 = multiHandLandmarks.length > 1 ? multiHandLandmarks[1] : null;

                const thumb = isThumbExtended(h1);
                const index = isFingerExtended(h1, 8, 6);
                const middle = isFingerExtended(h1, 12, 10);
                const ring = isFingerExtended(h1, 16, 14);
                const pinky = isFingerExtended(h1, 20, 18);
                const extCount = (thumb?1:0) + (index?1:0) + (middle?1:0) + (ring?1:0) + (pinky?1:0);

                const dThumbIndex = dist(h1[4], h1[8]);

                // Two-Handed Gestures (THANK YOU / EMERGENCY)
                if (h2) {{
                    const handsClose = dist(h1[0], h2[0]) < 0.35;
                    const h1Open = [8,12,16,20].filter(i => isFingerExtended(h1, i, i-2)).length >= 3;
                    const h2Open = [8,12,16,20].filter(i => isFingerExtended(h2, i, i-2)).length >= 3;

                    if (handsClose && h1Open && h2Open) {{
                        return {{ sign: "THANK_YOU", conf: 0.95 }};
                    }}
                }}

                // Single Hand Gestures
                // HELLO: Open 5 fingers spread
                if (extCount >= 4 && index && middle && ring && pinky) {{
                    return {{ sign: "HELLO", conf: 0.95 }};
                }}

                // YES: Thumbs up, other fingers curled
                if (thumb && !index && !middle && !ring && !pinky) {{
                    if (h1[4].y < h1[0].y) {{
                        return {{ sign: "YES", conf: 0.94 }};
                    }}
                }}

                // NO: Thumbs down or curled negation
                if (thumb && !index && !middle && !ring && !pinky) {{
                    if (h1[4].y > h1[0].y) {{
                        return {{ sign: "NO", conf: 0.93 }};
                    }}
                }}

                // GOOD: OK gesture (thumb & index touch, other fingers extended)
                if (dThumbIndex < 0.08 && middle && ring && pinky) {{
                    return {{ sign: "GOOD", conf: 0.95 }};
                }}

                // WATER: 3 fingers up (W shape: index, middle, ring)
                if (index && middle && ring && !pinky) {{
                    return {{ sign: "WATER", conf: 0.92 }};
                }}

                // HELP: Fist / hand curled near palm
                if (extCount <= 1 && thumb && h1[4].y < h1[0].y) {{
                    return {{ sign: "HELP", conf: 0.90 }};
                }}

                // HOSPITAL / DOCTOR / WHERE gestures
                if (index && middle && !ring && !pinky && !thumb) {{
                    return {{ sign: "HOSPITAL", conf: 0.91 }};
                }}

                if (index && !middle && !ring && !pinky && !thumb) {{
                    return {{ sign: "WHERE", conf: 0.90 }};
                }}

                return null;
            }}

            // Draw Skeleton on Canvas
            function drawHandSkeleton(landmarks) {{
                canvasCtx.save();
                canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

                if (!landmarks || landmarks.length === 0) {{
                    canvasCtx.restore();
                    return;
                }}

                const connections = [
                    [0,1],[1,2],[2,3],[3,4],
                    [0,5],[5,6],[6,7],[7,8],
                    [5,9],[9,10],[10,11],[11,12],
                    [9,13],[13,14],[14,15],[15,16],
                    [13,17],[17,18],[18,19],[19,20],[0,17]
                ];

                for (const hand of landmarks) {{
                    canvasCtx.strokeStyle = 'rgba(91, 92, 235, 0.85)';
                    canvasCtx.lineWidth = 3;

                    for (const [i, j] of connections) {{
                        canvasCtx.beginPath();
                        canvasCtx.moveTo(hand[i].x * canvasElement.width, hand[i].y * canvasElement.height);
                        canvasCtx.lineTo(hand[j].x * canvasElement.width, hand[j].y * canvasElement.height);
                        canvasCtx.stroke();
                    }}

                    for (const pt of hand) {{
                        canvasCtx.beginPath();
                        canvasCtx.arc(pt.x * canvasElement.width, pt.y * canvasElement.height, 4, 0, 2 * Math.PI);
                        canvasCtx.fillStyle = '#10B981';
                        canvasCtx.fill();
                    }}
                }}
                canvasCtx.restore();
            }}

            // =========================================================================
            // MEDIAPIPE INITIALIZATION (HANDS ONLY)
            // =========================================================================
            async function initMediaPipe() {{
                try {{
                    const hands = new Hands({{
                        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${{file}}`
                    }});

                    hands.setOptions({{
                        maxNumHands: 2,
                        modelComplexity: 1,
                        minDetectionConfidence: 0.65,
                        minTrackingConfidence: 0.60
                    }});

                    hands.onResults((results) => {{
                        if (canvasElement.width !== videoElement.videoWidth && videoElement.videoWidth > 0) {{
                            canvasElement.width = videoElement.videoWidth;
                            canvasElement.height = videoElement.videoHeight;
                        }}

                        const count = results.multiHandLandmarks ? results.multiHandLandmarks.length : 0;
                        handsCountHud.textContent = `Hands: ${{count}}`;

                        drawHandSkeleton(results.multiHandLandmarks);

                        if (count > 0) {{
                            reactionController.setState("LISTENING");
                            const rawPred = classifyHandAction(results.multiHandLandmarks);
                            if (rawPred) {{
                                frameBuffer.push(rawPred.sign);
                                if (frameBuffer.length > 8) frameBuffer.shift();

                                // Temporal voting: require consistent recognition
                                const counts = {{}};
                                frameBuffer.forEach(s => counts[s] = (counts[s] || 0) + 1);
                                const topSign = Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);

                                if (counts[topSign] >= 5) {{
                                    reactionController.reactToAction(topSign, rawPred.conf);
                                }}
                            }}
                        }} else {{
                            frameBuffer = [];
                            if (reactionController.state === "LISTENING") {{
                                reactionController.setState("READY");
                            }}
                        }}
                    }});

                    // Start Camera
                    const camera = new Camera(videoElement, {{
                        onFrame: async () => {{
                            await hands.send({{ image: videoElement }});
                        }},
                        width: 640,
                        height: 480
                    }});
                    await camera.start();
                }} catch (err) {{
                    console.warn("Webcam / MediaPipe initialization note:", err);
                    handsCountHud.textContent = "Webcam Inactive";
                }}
            }}

            window.addEventListener('DOMContentLoaded', () => {{
                updateTimelineUI();
                initMediaPipe();
            }});
        </script>
    </body>
    </html>
    """

    components.html(component_html, height=890, scrolling=False)
