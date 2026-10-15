"""
SUBWAY RUSH - Doraemon Edition (Characters & Difficulties)
Python + Streamlit + HTML5 Canvas + JavaScript
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Subway Rush - Doraemon",
    page_icon="🐱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: #0a0a1a; padding: 0 !important; margin: 0 !important;}
    .block-container {padding: 0 !important; max-width: 100% !important;}
    iframe {border: none !important;}
    div[data-testid="stToolbar"] {display: none;}
    section[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

GAME_HTML = r"""
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Subway Rush - Doraemon Edition</title>
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
    html, body {
        width: 100%; height: 100%; overflow: hidden;
        background: #0a0a1a; font-family: 'Segoe UI', system-ui, sans-serif;
        touch-action: none; user-select: none;
    }
    #gameContainer {
        position: relative; width: 100vw; height: 100vh;
        display: flex; justify-content: center; align-items: center;
        background: linear-gradient(180deg, #1a1a3e 0%, #0a0a1a 100%);
    }
    canvas {
        display: block; max-width: 100%; max-height: 100%;
        border-radius: 12px; box-shadow: 0 0 40px rgba(0,200,255,0.4);
        background: #111;
    }
    #ui {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 10;
    }
    #ui > * { pointer-events: auto; }
    .screen {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        background: linear-gradient(135deg, #1a0033 0%, #000033 50%, #001a33 100%);
        color: #fff; text-align: center; padding: 20px;
    }
    .screen.hidden { display: none; }
    .logo {
        font-size: clamp(2rem, 7vw, 3.5rem); font-weight: 900;
        background: linear-gradient(90deg, #00ffff, #ff00aa, #ffff00);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 30px rgba(0,255,255,0.5);
        margin-bottom: 6px; letter-spacing: 2px;
    }
    .subtitle { color: #aaa; margin-bottom: 20px; font-size: 0.95rem; }
    .btn {
        background: linear-gradient(90deg, #ff00aa, #00ccff);
        border: none; color: #fff; font-size: 1.1rem; font-weight: 700;
        padding: 12px 40px; margin: 6px; border-radius: 50px;
        cursor: pointer; transition: transform 0.15s, box-shadow 0.15s;
        box-shadow: 0 4px 20px rgba(255,0,170,0.4);
        min-width: 220px;
    }
    .btn:hover, .btn:active { transform: scale(1.05); box-shadow: 0 6px 28px rgba(0,200,255,0.6); }
    .btn.secondary {
        background: linear-gradient(90deg, #333, #555);
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .btn.small { padding: 8px 24px; font-size: 0.9rem; min-width: 130px; }
    .difficulty-group {
        display: flex; gap: 8px; margin: 10px 0; justify-content: center;
    }
    .diff-btn {
        background: rgba(255,255,255,0.1); border: 2px solid rgba(255,255,255,0.3);
        color: #fff; padding: 8px 16px; border-radius: 20px; cursor: pointer; font-weight: 600;
    }
    .diff-btn.active { background: #00ccff; border-color: #fff; color: #000; box-shadow: 0 0 15px #00ccff; }
    .stats-bar {
        position: absolute; top: 12px; left: 0; right: 0;
        display: flex; justify-content: space-around; align-items: center;
        padding: 8px 16px; background: rgba(0,0,0,0.6);
        backdrop-filter: blur(8px); border-radius: 0 0 16px 16px;
        font-size: 0.95rem; font-weight: 600; color: #fff;
        pointer-events: none;
    }
    .stat { display: flex; align-items: center; gap: 6px; }
    .stat span { color: #00ffff; }
    #touchControls {
        position: absolute; bottom: 20px; left: 0; right: 0;
        display: none; justify-content: center; gap: 12px;
        pointer-events: none;
    }
    .touch-btn {
        width: 64px; height: 64px; border-radius: 50%;
        background: rgba(255,255,255,0.15); border: 2px solid rgba(255,255,255,0.35);
        color: #fff; font-size: 1.6rem; display: flex;
        justify-content: center; align-items: center;
        pointer-events: auto; backdrop-filter: blur(4px);
    }
    .touch-btn:active { background: rgba(0,200,255,0.4); }
    #hudButtons {
        position: absolute; top: 60px; right: 12px;
        display: none; flex-direction: column; gap: 8px;
    }
    .hud-btn {
        width: 44px; height: 44px; border-radius: 50%;
        background: rgba(0,0,0,0.5); border: 2px solid rgba(255,255,255,0.3);
        color: #fff; font-size: 1.2rem; cursor: pointer;
        display: flex; justify-content: center; align-items: center;
    }
    .list-box {
        max-height: 45vh; overflow-y: auto; width: 90%; max-width: 360px;
        margin: 12px 0; text-align: left;
    }
    .list-item {
        background: rgba(255,255,255,0.08); border-radius: 12px;
        padding: 12px 16px; margin: 8px 0; display: flex;
        justify-content: space-between; align-items: center;
        border: 1px solid rgba(255,255,255,0.1); cursor: pointer;
    }
    .list-item.selected { border-color: #00ff99; background: rgba(0,255,153,0.15); }
    .powerup-icons {
        position: absolute; bottom: 100px; left: 12px;
        display: flex; gap: 8px; pointer-events: none;
    }
    .powerup-icon {
        width: 40px; height: 40px; border-radius: 8px;
        background: rgba(0,0,0,0.5); border: 2px solid #fff;
        display: flex; justify-content: center; align-items: center;
        font-size: 1.2rem; opacity: 0.3;
    }
    .powerup-icon.active { opacity: 1; border-color: #00ff99; box-shadow: 0 0 12px #00ff99; }
    @media (max-width: 600px) {
        .btn { min-width: 160px; padding: 10px 28px; font-size: 1rem; }
        #touchControls { display: flex; }
    }
</style>
</head>
<body>
<div id="gameContainer">
    <canvas id="gameCanvas" width="480" height="720"></canvas>
    <div id="ui">
        <!-- MAIN MENU -->
        <div id="menuScreen" class="screen">
            <div class="logo">SUBWAY RUSH</div>
            <div class="subtitle">Thế Giới Hoạt Hình</div>
            <div style="margin-bottom:12px;font-size:1.05rem;">
                🏆 Kỷ lục: <span id="menuHighScore">0</span> &nbsp;|&nbsp; 🪙 <span id="menuCoins">0</span>
            </div>
            
            <div style="margin-bottom:8px; font-size:0.9rem; color:#00ffff;">Chọn Độ Khó:</div>
            <div class="difficulty-group">
                <button class="diff-btn active" id="diffEasy" onclick="setDifficulty('easy')">Dễ</button>
                <button class="diff-btn" id="diffNormal" onclick="setDifficulty('normal')">Bình Thường</button>
                <button class="diff-btn" id="diffHard" onclick="setDifficulty('hard')">Khó</button>
            </div>

            <button class="btn" onclick="startGame()" style="margin-top:12px;">▶ BẮT ĐẦU CHƠI</button>
            <button class="btn secondary" onclick="showScreen('charScreen')">👤 CHỌN NHÂN VẬT</button>
            <button class="btn secondary" onclick="showScreen('settingsScreen')">⚙ CÀI ĐẶT</button>
        </div>

        <!-- CHARACTER SELECTION -->
        <div id="charScreen" class="screen hidden">
            <div class="logo" style="font-size:1.8rem;">CHỌN NHÂN VẬT</div>
            <div class="list-box" id="charList"></div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← QUAY LẠI</button>
        </div>

        <!-- SETTINGS -->
        <div id="settingsScreen" class="screen hidden">
            <div class="logo" style="font-size:1.8rem;">CÀI ĐẶT</div>
            <div style="margin:20px 0; text-align:left;">
                <label style="display:block;margin:14px 0; font-size:1.1rem;">
                    Âm thanh: <input type="checkbox" id="soundToggle" checked onchange="toggleSound()">
                </label>
                <label style="display:block;margin:14px 0; font-size:1.1rem;">
                    Rung: <input type="checkbox" id="vibToggle" checked>
                </label>
            </div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← QUAY LẠI</button>
        </div>

        <!-- GAME OVER -->
        <div id="gameOverScreen" class="screen hidden">
            <div class="logo" style="font-size:2.2rem;">THUA RỒI!</div>
            <div style="font-size:1.3rem;margin:14px 0;">
                Điểm số: <span id="finalScore" style="color:#00ffff;">0</span>
            </div>
            <div style="margin-bottom:6px;">Xu thu thập: <span id="finalCoins">0</span></div>
            <div style="margin-bottom:18px;">Kỷ lục mới: <span id="finalHigh">0</span></div>
            <button class="btn" onclick="startGame()">↻ CHƠI LẠI</button>
            <button class="btn secondary" onclick="showScreen('menuScreen')">⌂ MENU CHÍNH</button>
        </div>

        <!-- PAUSE -->
        <div id="pauseScreen" class="screen hidden" style="background:rgba(0,0,0,0.75);">
            <div class="logo" style="font-size:2.2rem;">TẠM DỪNG</div>
            <button class="btn" onclick="resumeGame()">▶ TIẾP TỤC</button>
            <button class="btn secondary" onclick="quitToMenu()">⌂ THOÁT</button>
        </div>

        <!-- HUD -->
        <div id="statsBar" class="stats-bar" style="display:none;">
            <div class="stat">⭐ <span id="hudScore">0</span></div>
            <div class="stat">🪙 <span id="hudCoins">0</span></div>
            <div class="stat">🏆 <span id="hudHigh">0</span></div>
        </div>
        <div id="hudButtons" style="display:none;">
            <button class="hud-btn" onclick="pauseGame()">⏸</button>
        </div>
        <div id="powerupIcons" class="powerup-icons" style="display:none;">
            <div class="powerup-icon" id="puMagnet" title="Hút xu">🧲</div>
            <div class="powerup-icon" id="puJump" title="Nhảy cao">👟</div>
            <div class="powerup-icon" id="puScore" title="Nhân đôi điểm">✖2</div>
            <div class="powerup-icon" id="puShield" title="Khiên bảo vệ">🛡</div>
        </div>
        <div id="touchControls">
            <button class="touch-btn" ontouchstart="handleTouch('left')" onmousedown="handleTouch('left')">◀</button>
            <button class="touch-btn" ontouchstart="handleTouch('up')" onmousedown="handleTouch('up')">▲</button>
            <button class="touch-btn" ontouchstart="handleTouch('down')" onmousedown="handleTouch('down')">▼</button>
            <button class="touch-btn" ontouchstart="handleTouch('right')" onmousedown="handleTouch('right')">▶</button>
        </div>
    </div>
</div>

<script>
// ==================== AUDIO SYSTEM ====================
let audioCtx = null;
let bgmTimer = null;

function initAudio() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (audioCtx.state === 'suspended') audioCtx.resume();
}

function playSound(type) {
    if (!save.sound) return;
    initAudio();
    if (!audioCtx) return;
    const now = audioCtx.currentTime;

    if (type === 'jump') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.frequency.setValueAtTime(200, now);
        osc.frequency.exponentialRampToValueAtTime(500, now + 0.15);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.15);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'coin') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.frequency.setValueAtTime(987.77, now);
        osc.frequency.setValueAtTime(1318.51, now + 0.05);
        gain.gain.setValueAtTime(0.15, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.15);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.15);
    } else if (type === 'hit') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, now);
        osc.frequency.linearRampToValueAtTime(40, now + 0.3);
        gain.gain.setValueAtTime(0.3, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.3);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.3);
    }
}

function startBGM() {
    stopBGM();
    if (!save.sound) return;
    initAudio();
    if (!audioCtx) return;
    let idx = 0;
    const notes = [330, 392, 440, 523, 440, 392];
    bgmTimer = setInterval(() => {
        if (state !== 'playing' || !save.sound) return;
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(notes[idx], now);
        gain.gain.setValueAtTime(0.04, now);
        gain.gain.linearRampToValueAtTime(0, now + 0.12);
        osc.connect(gain); gain.connect(audioCtx.destination);
        osc.start(now); osc.stop(now + 0.12);
        idx = (idx + 1) % notes.length;
    }, 180);
}

function stopBGM() {
    if (bgmTimer) { clearInterval(bgmTimer); bgmTimer = null; }
}

// ==================== SAVE DATA ====================
const STORAGE_KEY = 'subwayRushDoraemon_v1';
let save = {
    highScore: 0,
    coins: 0,
    currentChar: 0, // 0: Nobita, 1: Doraemon, 2: Shizuka
    difficulty: 'normal', // easy, normal, hard
    sound: true,
    vibration: true
};

function loadSave() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) Object.assign(save, JSON.parse(raw));
    } catch(e) {}
    updateMenuStats();
    setDifficultyUI(save.difficulty);
}
function persist() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(save)); } catch(e) {}
}

// Characters definition
const CHARACTERS = [
    { id: 0, name: 'Nobita', desc: 'Áo đỏ, mắt kính quen thuộc[cite: 3]', color: '#ff4444', shirt: '#ff3333', pants: '#0066cc' },
    { id: 1, name: 'Doraemon', desc: 'Mèo máy thông minh, chuông vàng[cite: 4]', color: '#0099ff', shirt: '#0099ff', pants: '#ff3333' },
    { id: 2, name: 'Shizuka', desc: 'Dịu dàng, áo hồng váy xanh[cite: 5]', color: '#ff66aa', shirt: '#ff66aa', pants: '#0066cc' }
];

// Difficulty settings
const DIFFICULTIES = {
    easy: { initialSpeed: 5, speedInc: 0.25, spawnRate: 65 },
    normal: { initialSpeed: 6.5, speedInc: 0.35, spawnRate: 50 },
    hard: { initialSpeed: 8, speedInc: 0.5, spawnRate: 38 }
};

function setDifficulty(diff) {
    save.difficulty = diff;
    persist();
    setDifficultyUI(diff);
}

function setDifficultyUI(diff) {
    ['easy', 'normal', 'hard'].forEach(d => {
        const btn = document.getElementById('diff' + d.charAt(0).toUpperCase() + d.slice(1));
        if (btn) btn.classList.toggle('active', d === diff);
    });
}

// ==================== GAME STATE ====================
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W = 480, H = 720;
const LANES = [W * 0.25, W * 0.5, W * 0.75];

let state = 'menu';
let player, obstacles, coins, powerups, particles;
let score = 0, runCoins = 0, distance = 0, speed = 6.5;
let combo = 0, lastCoinTime = 0;
let gameTime = 0, frame = 0;
let activePowerups = { magnet: 0, jump: 0, scorex2: 0, shield: 0 };
let invincible = 0;
let keys = {};
let touchStartX = 0, touchStartY = 0;

function createPlayer() {
    return {
        lane: 1, x: LANES[1], y: H * 0.72, targetX: LANES[1],
        width: 38, height: 58,
        jumping: false, jumpY: 0, jumpVel: 0,
        sliding: false, slideTimer: 0, animFrame: 0
    };
}

function spawnObstacle() {
    const lane = Math.floor(Math.random() * 3);
    const types = ['train', 'barrier', 'box', 'lowbarrier'];
    const type = types[Math.floor(Math.random() * types.length)];
    let h = 75, w = 52;
    if (type === 'train') { h = 115; w = 60; }
    else if (type === 'lowbarrier') { h = 36; w = 50; }
    obstacles.push({ lane, x: LANES[lane], y: -130, type, w, h, passed: false });
}

function spawnCoin() {
    const lane = Math.floor(Math.random() * 3);
    coins.push({ lane, x: LANES[lane], y: -40, r: 12 });
}

function spawnPowerup() {
    if (Math.random() > 0.015) return;
    const types = ['magnet', 'jump', 'scorex2', 'shield'];
    const type = types[Math.floor(Math.random() * types.length)];
    const lane = Math.floor(Math.random() * 3);
    powerups.push({ lane, x: LANES[lane], y: -50, type, r: 18 });
}

// Input listeners
document.addEventListener('keydown', e => {
    initAudio();
    if (state === 'playing') {
        if (e.code === 'ArrowLeft' || e.code === 'KeyA') moveLane(-1);
        if (e.code === 'ArrowRight' || e.code === 'KeyD') moveLane(1);
        if (e.code === 'ArrowUp' || e.code === 'KeyW' || e.code === 'Space') jump();
        if (e.code === 'ArrowDown' || e.code === 'KeyS') slide();
        if (e.code === 'Escape' || e.code === 'KeyP') pauseGame();
    }
    e.preventDefault();
});

canvas.addEventListener('touchstart', e => {
    initAudio();
    const t = e.changedTouches[0];
    touchStartX = t.clientX; touchStartY = t.clientY;
}, { passive: true });

canvas.addEventListener('touchend', e => {
    if (state !== 'playing') return;
    const t = e.changedTouches[0];
    const dx = t.clientX - touchStartX;
    const dy = t.clientY - touchStartY;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 30) {
        moveLane(dx > 0 ? 1 : -1);
    } else if (Math.abs(dy) > 30) {
        if (dy < 0) jump(); else slide();
    }
}, { passive: true });

function handleTouch(dir) {
    initAudio();
    if (state !== 'playing') return;
    if (dir === 'left') moveLane(-1);
    if (dir === 'right') moveLane(1);
    if (dir === 'up') jump();
    if (dir === 'down') slide();
}

function moveLane(dir) {
    if (player.sliding) return;
    const newLane = Math.max(0, Math.min(2, player.lane + dir));
    if (newLane !== player.lane) {
        player.lane = newLane;
        player.targetX = LANES[newLane];
    }
}
function jump() {
    if (!player.jumping && !player.sliding) {
        player.jumping = true;
        player.jumpVel = activePowerups.jump > 0 ? -17 : -14;
        playSound('jump');
    }
}
function slide() {
    if (!player.jumping && !player.sliding) {
        player.sliding = true;
        player.slideTimer = 25;
    }
}

// Game Flow
function startGame() {
    initAudio();
    const diffSetting = DIFFICULTIES[save.difficulty] || DIFFICULTIES.normal;
    player = createPlayer();
    obstacles = []; coins = []; powerups = []; particles = [];
    score = 0; runCoins = 0; distance = 0; speed = diffSetting.initialSpeed;
    combo = 0; gameTime = 0; frame = 0;
    activePowerups = { magnet: 0, jump: 0, scorex2: 0, shield: 0 };
    invincible = 60;
    state = 'playing';
    showScreen(null);
    document.