"""
SUBWAY RUSH - Doraemon Ultimate Edition (Refined Characters)
Python + Streamlit + HTML5 Canvas + JavaScript
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Subway Rush - Doraemon Ultimate",
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
<title>Subway Rush - Doraemon Ultimate</title>
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
        border: 1px solid rgba(255,255,255,0.1);
    }
    .list-item.selected { border-color: #00ff99; background: rgba(0,255,153,0.15); }
    .progress-bar {
        width: 100%; height: 6px; background: #333; border-radius: 3px; overflow: hidden; margin-top: 6px;
    }
    .progress-fill { height: 100%; background: linear-gradient(90deg,#00ff99,#00ccff); transition: width 0.3s; }
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
            <div class="subtitle">Doraemon Ultimate Edition</div>
            <div style="margin-bottom:10px;font-size:1.05rem;">
                🏆 Kỷ lục (<span id="diffLabel">Thường</span>): <span id="menuHighScore">0</span> &nbsp;|&nbsp; 🪙 <span id="menuCoins">0</span>
            </div>
            
            <div style="margin-bottom:6px; font-size:0.9rem; color:#00ffff;">Chọn Độ Khó:</div>
            <div class="difficulty-group">
                <button class="diff-btn active" id="diffEasy" onclick="setDifficulty('easy')">Dễ</button>
                <button class="diff-btn" id="diffNormal" onclick="setDifficulty('normal')">Bình Thường</button>
                <button class="diff-btn" id="diffHard" onclick="setDifficulty('hard')">Khó</button>
            </div>

            <button class="btn" onclick="startGame()" style="margin-top:10px;">▶ BẮT ĐẦU CHƠI</button>
            <button class="btn secondary" onclick="showScreen('charScreen')">👤 NHÂN VẬT</button>
            <button class="btn secondary" onclick="showScreen('missionsScreen')">📋 NHIỆM VỤ</button>
            <button class="btn secondary" onclick="showScreen('settingsScreen')">⚙ CÀI ĐẶT</button>
        </div>

        <!-- CHARACTER SELECTION -->
        <div id="charScreen" class="screen hidden">
            <div class="logo" style="font-size:1.8rem;">CHỌN NHÂN VẬT</div>
            <div class="list-box" id="charList"></div>
            <button class="btn secondary small" onclick="showScreen('menuScreen')">← QUAY LẠI</button>
        </div>

        <!-- MISSIONS -->
        <div id="missionsScreen" class="screen hidden">
            <div class="logo" style="font-size:1.8rem;">NHIỆM VỤ</div>
            <div class="list-box" id="missionsList"></div>
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
            <div style="margin-bottom:18px;">Kỷ lục chế độ: <span id="finalHigh">0</span> <span id="newRecordBadge" style="color:#00ff99;font-weight:bold;display:none;">(KỶ LỤC MỚI! 🎉)</span></div>
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
            <div class="powerup-icon" id="puCopter" title="Chong chóng tre">🚁</div>
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

const STORAGE_KEY = 'subwayRushDoraemonRecords_v3';
let save = {
    highScores: { easy: 0, normal: 0, hard: 0 },
    coins: 0,
    currentChar: 0,
    difficulty: 'normal',
    sound: true,
    vibration: true,
    missions: [
        { id: 1, name: 'Nhặt 30 đồng xu', target: 30, progress: 0, reward: 100, claimed: false },
        { id: 2, name: 'Đạt 300 điểm số', target: 300, progress: 0, reward: 150, claimed: false }
    ]
};

function loadSave() {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) {
            const data = JSON.parse(raw);
            Object.assign(save, data);
            if (typeof save.highScores !== 'object') {
                save.highScores = { easy: 0, normal: data.highScore || 0, hard: 0 };
            }
        }
    } catch(e) {}
    updateMenuStats();
    setDifficultyUI(save.difficulty);
}

function persist() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(save)); } catch(e) {}
}

const CHARACTERS = [
    { id: 0, name: 'Nobita', desc: 'Áo đỏ, mắt kính quen thuộc[cite: 3]' },
    { id: 1, name: 'Doraemon', desc: 'Mèo máy thông minh, chuông vàng[cite: 4]' },
    { id: 2, name: 'Shizuka', desc: 'Dịu dàng, áo hồng váy xanh[cite: 5]' }
];

const DIFFICULTIES = {
    easy: { name: 'Dễ', initialSpeed: 5, speedInc: 0.25, spawnRate: 65 },
    normal: { name: 'Bình Thường', initialSpeed: 6.5, speedInc: 0.35, spawnRate: 50 },
    hard: { name: 'Khó', initialSpeed: 8, speedInc: 0.5, spawnRate: 38 }
};

function setDifficulty(diff) {
    save.difficulty = diff;
    persist();
    setDifficultyUI(diff);
    updateMenuStats();
}

function setDifficultyUI(diff) {
    ['easy', 'normal', 'hard'].forEach(d => {
        const btn = document.getElementById('diff' + d.charAt(0).toUpperCase() + d.slice(1));
        if (btn) btn.classList.toggle('active', d === diff);
    });
    const label = document.getElementById('diffLabel');
    if (label) label.textContent = DIFFICULTIES[diff].name;
}

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let W = 480, H = 720;
const LANES = [W * 0.25, W * 0.5, W * 0.75];

let state = 'menu';
let player, obstacles, coins, powerups, particles;
let score = 0, runCoins = 0, distance = 0, speed = 6.5;
let combo = 0, lastCoinTime = 0;
let gameTime = 0, frame = 0;
let activePowerups = { magnet: 0, copter: 0, scorex2: 0, shield: 0 };
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
    const types = ['magnet', 'copter', 'scorex2', 'shield'];
    const type = types[Math.floor(Math.random() * types.length)];
    const lane = Math.floor(Math.random() * 3);
    powerups.push({ lane, x: LANES[lane], y: -50, type, r: 18 });
}

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
        player.jumpVel = activePowerups.copter > 0 ? -18 : -14;
        playSound('jump');
    }
}
function slide() {
    if (!player.jumping && !player.sliding && activePowerups.copter <= 0) {
        player.sliding = true;
        player.slideTimer = 25;
    }
}

function startGame() {
    initAudio();
    const diffSetting = DIFFICULTIES[save.difficulty] || DIFFICULTIES.normal;
    player = createPlayer();
    obstacles = []; coins = []; powerups = []; particles = [];
    score = 0; runCoins = 0; distance = 0; speed = diffSetting.initialSpeed;
    combo = 0; gameTime = 0; frame = 0;
    activePowerups = { magnet: 0, copter: 0, scorex2: 0, shield: 0 };
    invincible = 60;
    state = 'playing';
    showScreen(null);
    document.getElementById('statsBar').style.display = 'flex';
    document.getElementById('hudButtons').style.display = 'flex';
    document.getElementById('powerupIcons').style.display = 'flex';
    updateHud();
    startBGM();
    requestAnimationFrame(loop);
}

function pauseGame() {
    if (state === 'playing') {
        state = 'paused'; stopBGM();
        document.getElementById('pauseScreen').classList.remove('hidden');
    }
}
function resumeGame() {
    if (state === 'paused') {
        state = 'playing'; startBGM();
        document.getElementById('pauseScreen').classList.add('hidden');
        requestAnimationFrame(loop);
    }
}
function quitToMenu() {
    state = 'menu'; stopBGM();
    document.getElementById('pauseScreen').classList.add('hidden');
    document.getElementById('statsBar').style.display = 'none';
    document.getElementById('hudButtons').style.display = 'none';
    document.getElementById('powerupIcons').style.display = 'none';
    showScreen('menuScreen');
    updateMenuStats();
}

function gameOver() {
    state = 'gameover'; stopBGM(); playSound('hit');
    
    const currentDiff = save.difficulty;
    const currentHighScore = save.highScores[currentDiff] || 0;
    let isNewRecord = false;
    
    const finalScoreInt = Math.floor(score);
    if (finalScoreInt > currentHighScore) {
        save.highScores[currentDiff] = finalScoreInt;
        isNewRecord = true;
    }
    
    save.coins += runCoins;
    
    save.missions.forEach(m => {
        if (m.id === 1) m.progress += runCoins;
        if (m.id === 2) m.progress = Math.max(m.progress, finalScoreInt);
    });
    
    persist();
    
    document.getElementById('finalScore').textContent = finalScoreInt;
    document.getElementById('finalCoins').textContent = runCoins;
    document.getElementById('finalHigh').textContent = save.highScores[currentDiff];
    document.getElementById('newRecordBadge').style.display = isNewRecord ? 'inline' : 'none';
    
    document.getElementById('statsBar').style.display = 'none';
    document.getElementById('hudButtons').style.display = 'none';
    document.getElementById('powerupIcons').style.display = 'none';
    document.getElementById('gameOverScreen').classList.remove('hidden');
    
    updateMenuStats();
    if (save.vibration && navigator.vibrate) navigator.vibrate([80, 40, 80]);
}

function update() {
    if (state !== 'playing') return;
    frame++;
    const diffSetting = DIFFICULTIES[save.difficulty] || DIFFICULTIES.normal;
    gameTime += 1/60;
    distance += speed;
    score += (speed * 0.15) * (activePowerups.scorex2 > 0 ? 2 : 1);
    
    const currentHigh = save.highScores[save.difficulty] || 0;
    if (score > currentHigh) {
        save.highScores[save.difficulty] = Math.floor(score);
    }

    if (frame % 300 === 0) speed = Math.min(speed + diffSetting.speedInc, 16);

    player.x += (player.targetX - player.x) * 0.25;
    player.animFrame = (player.animFrame + 0.3) % 4;

    if (activePowerups.copter > 0) {
        player.jumpY = -60;
        player.jumping = false;
        player.sliding = false;
    } else if (player.jumping) {
        player.jumpVel += 0.75;
        player.jumpY += player.jumpVel;
        if (player.jumpY >= 0) { player.jumpY = 0; player.jumping = false; player.jumpVel = 0; }
    }
    if (player.sliding) {
        player.slideTimer--;
        if (player.slideTimer <= 0) player.sliding = false;
    }

    if (frame % Math.max(20, diffSetting.spawnRate - Math.floor(speed * 1.5)) === 0) spawnObstacle();
    if (frame % 16 === 0) spawnCoin();
    spawnPowerup();

    for (let i = obstacles.length - 1; i >= 0; i--) {
        const o = obstacles[i];
        o.y += speed;
        if (o.y > H + 60) { obstacles.splice(i, 1); continue; }
        if (invincible <= 0 && activePowerups.copter <= 0 && !o.passed) {
            const px = player.x, py = player.y + player.jumpY;
            const pw = player.width, ph = player.sliding ? player.height * 0.45 : player.height;
            const pyAdj = player.sliding ? py + player.height * 0.55 : py;
            if (Math.abs(px - o.x) < (pw + o.w) * 0.4 && pyAdj < o.y + o.h && pyAdj + ph > o.y) {
                let hit = true;
                if (o.type === 'lowbarrier' && player.jumping && player.jumpY < -20) hit = false;
                if ((o.type === 'barrier' || o.type === 'train') && player.sliding) hit = false;
                if (hit) {
                    if (activePowerups.shield > 0) {
                        activePowerups.shield = 0; invincible = 90; playSound('hit');
                        createParticles(px, py, '#00ff99');
                    } else { gameOver(); return; }
                }
            }
        }
    }

    for (let i = coins.length - 1; i >= 0; i--) {
        const c = coins[i];
        c.y += speed;
        if (activePowerups.magnet > 0) {
            const dx = player.x - c.x, dy = (player.y + player.jumpY) - c.y;
            const dist = Math.sqrt(dx*dx + dy*dy);
            if (dist < 200) { c.x += dx * 0.15; c.y += dy * 0.15; }
        }
        if (c.y > H + 30) { coins.splice(i, 1); continue; }
        const px = player.x, py = player.y + player.jumpY;
        if (Math.abs(px - c.x) < 32 && Math.abs(py - c.y) < 42) {
            coins.splice(i, 1); runCoins++; combo++; lastCoinTime = frame;
            score += 10 * (activePowerups.scorex2 > 0 ? 2 : 1) * Math.min(combo, 5);
            playSound('coin');
            createParticles(c.x, c.y, '#ffcc00');
        }
    }
    if (frame - lastCoinTime > 40) combo = 0;

    for (let i = powerups.length - 1; i >= 0; i--) {
        const p = powerups[i];
        p.y += speed;
        if (p.y > H + 30) { powerups.splice(i, 1); continue; }
        const px = player.x, py = player.y + player.jumpY;
        if (Math.abs(px - p.x) < 35 && Math.abs(py - p.y) < 40) {
            powerups.splice(i, 1);
            if (p.type === 'magnet') activePowerups.magnet = 350;
            if (p.type === 'copter') activePowerups.copter = 250;
            if (p.type === 'scorex2') activePowerups.scorex2 = 300;
            if (p.type === 'shield') activePowerups.shield = 250;
            playSound('coin');
            createParticles(c.x, c.y, '#00ff99');
        }
    }

    if (invincible > 0) invincible--;
    for (let k in activePowerups) { if (activePowerups[k] > 0) activePowerups[k]--; }

    for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.x += p.vx; p.y += p.vy; p.life--;
        if (p.life <= 0) particles.splice(i, 1);
    }

    updateHud();
    updatePowerupIcons();
}

function createParticles(x, y, color) {
    for (let i = 0; i < 10; i++) {
        particles.push({
            x, y, vx: (Math.random() - 0.5) * 7, vy: (Math.random() - 0.5) * 7 - 2,
            life: 25 + Math.random() * 15, color, size: 3 + Math.random() * 4
        });
    }
}

function draw() {
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    if (distance > 2500) {
        grad.addColorStop(0, '#05021a'); grad.addColorStop(0.5, '#120b35'); grad.addColorStop(1, '#1b1448');
    } else {
        grad.addColorStop(0, '#0f0c29'); grad.addColorStop(0.5, '#302b63'); grad.addColorStop(1, '#24243e');
    }
    ctx.fillStyle = grad; ctx.fillRect(0, 0, W, H);

    drawBuildings();
    drawTracks();

    coins.forEach(c => drawCoin(c));
    powerups.forEach(p => drawPowerup(p));
    obstacles.forEach(o => drawObstacle(o));

    if (state === 'playing' || state === 'paused') drawPlayer();

    particles.forEach(p => {
        ctx.globalAlpha = p.life / 40;
        ctx.fillStyle = p.color;
        ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
        ctx.globalAlpha = 1;
    });
}

function drawBuildings() {
    const offset = (distance * 0.25) % 130;
    ctx.fillStyle = '#161638';
    for (let i = -1; i < 8; i++) {
        const x = i * 75 - offset;
        const h = 90 + (Math.sin(i * 1.5) * 45 + 45);
        ctx.fillRect(x, H * 0.35 - h, 60, h);
        ctx.fillStyle = '#22325c';
        for (let wy = 5; wy < h - 10; wy += 16) {
            for (let wx = 10; wx < 50; wx += 14) {
                if (Math.random() > 0.25) ctx.fillRect(x + wx, H * 0.35 - h + wy, 6, 9);
            }
        }
        ctx.fillStyle = '#161638';
    }
}

function drawTracks() {
    ctx.fillStyle = '#1e1e2f';
    ctx.fillRect(0, H * 0.55, W, H * 0.45);
    const railOffset = (distance * 1.3) % 45;
    ctx.strokeStyle = '#666'; ctx.lineWidth = 4;
    for (let l = 0; l < 3; l++) {
        ctx.beginPath(); ctx.moveTo(LANES[l] - 32, H * 0.55); ctx.lineTo(LANES[l] - 32, H); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(LANES[l] + 32, H * 0.55); ctx.lineTo(LANES[l] + 32, H); ctx.stroke();
    }
    ctx.fillStyle = '#3a2e2b';
    for (let y = H * 0.55 - railOffset; y < H; y += 45) {
        for (let l = 0; l < 3; l++) ctx.fillRect(LANES[l] - 38, y, 76, 11);
    }
}

// ==================== REFINED CHARACTERS RENDERING ====================
function drawPlayer() {
    const px = player.x, py = player.y + player.jumpY;
    const ph = player.sliding ? player.height * 0.48 : player.height;
    const pyDraw = player.sliding ? py + player.height * 0.52 : py;

    ctx.save();
    if (invincible > 0 && Math.floor(frame / 4) % 2 === 0) ctx.globalAlpha = 0.5;

    // Shadow
    ctx.fillStyle = 'rgba(0,0,0,0.4)';
    ctx.beginPath(); ctx.ellipse(px, player.y + player.height + 6, 20, 8, 0, 0, Math.PI * 2); ctx.fill();

    if (save.currentChar === 1) {
        // --- DORAEMON ---
        // Body (Blue jumpsuit)
        ctx.fillStyle = '#007acc';
        roundRect(px - 18, pyDraw + 10, 36, ph - 10, 14);
        // White tummy pocket circle
        ctx.fillStyle = '#ffffff';
        ctx.beginPath(); ctx.arc(px, pyDraw + ph * 0.55, 13, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#cccccc'; ctx.lineWidth = 1; ctx.stroke();
        // Pocket opening
        ctx.beginPath(); ctx.arc(px, pyDraw + ph * 0.57, 8, 0, Math.PI, false); ctx.stroke();
        // Red collar & Yellow bell
        ctx.fillStyle = '#e60000'; ctx.fillRect(px - 17, pyDraw + 6, 34, 6);
        ctx.fillStyle = '#ffd700'; ctx.beginPath(); ctx.arc(px, pyDraw + 14, 5, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#b39700'; ctx.lineWidth = 1; ctx.stroke();
        // Head (Big blue sphere)
        ctx.fillStyle = '#0080ff'; ctx.beginPath(); ctx.arc(px, pyDraw - 8, 20, 0, Math.PI * 2); ctx.fill();
        // White face area
        ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.arc(px, pyDraw - 5, 15, 0, Math.PI * 2); ctx.fill();
        // Red nose & Whiskers
        ctx.fillStyle = '#ff0000'; ctx.beginPath(); ctx.arc(px, pyDraw - 10, 4, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#333333'; ctx.lineWidth = 1.5;
        ctx.beginPath();
        // Whiskers left
        ctx.moveTo(px - 4, pyDraw - 8); ctx.lineTo(px - 12, pyDraw - 9);
        ctx.moveTo(px - 4, pyDraw - 6); ctx.lineTo(px - 12, pyDraw - 5);
        // Whiskers right
        ctx.moveTo(px + 4, pyDraw - 8); ctx.lineTo(px + 12, pyDraw - 9);
        ctx.moveTo(px + 4, pyDraw - 6); ctx.lineTo(px + 12, pyDraw - 5);
        ctx.stroke();
        // Eyes
        ctx.fillStyle = '#ffffff'; ctx.strokeStyle = '#333'; ctx.lineWidth = 1.5;
        ctx.beginPath(); ctx.ellipse(px - 5, pyDraw - 17, 5, 7, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.beginPath(); ctx.ellipse(px + 5, pyDraw - 17, 5, 7, 0, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#111';
        ctx.beginPath(); ctx.arc(px - 4, pyDraw - 16, 2, 0, Math.PI * 2); ctx.arc(px + 6, pyDraw - 16, 2, 0, Math.PI * 2); ctx.fill();

    } else if (save.currentChar === 2) {
        // --- SHIZUKA ---
        // Pink shirt & Blue skirt
        ctx.fillStyle = '#ff66aa'; roundRect(px - 15, pyDraw + 10, 30, ph - 18, 6);
        ctx.fillStyle = '#0066cc'; roundRect(px - 16, pyDraw + ph - 22, 32, 22, 4);
        // White collar
        ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(px, pyDraw + 12); ctx.lineTo(px - 8, pyDraw + 8); ctx.lineTo(px + 8, pyDraw + 8); ctx.closePath(); ctx.fill();
        // Head & Face
        ctx.fillStyle = '#ffdbac'; ctx.beginPath(); ctx.arc(px, pyDraw - 4, 14, 0, Math.PI * 2); ctx.fill();
        // Hair (Pigtails)
        ctx.fillStyle = '#222222';
        ctx.beginPath(); ctx.arc(px, pyDraw - 8, 13, Math.PI, Math.PI * 2); ctx.fill();
        ctx.beginPath(); ctx.arc(px - 14, pyDraw - 2, 6, 0, Math.PI * 2); ctx.arc(px + 14, pyDraw - 2, 6, 0, Math.PI * 2); ctx.fill();
        // Eyes
        ctx.fillStyle = '#222222'; ctx.beginPath(); ctx.arc(px - 4, pyDraw - 5, 2, 0, Math.PI * 2); ctx.arc(px + 4, pyDraw - 5, 2, 0, Math.PI * 2); ctx.fill();

    } else {
        // --- NOBITA ---
        // Red long-sleeve shirt & Blue shorts
        ctx.fillStyle = '#e60000'; roundRect(px - 15, pyDraw + 10, 30, ph - 18, 6);
        ctx.fillStyle = '#0066cc'; roundRect(px - 15, pyDraw + ph - 22, 30, 22, 4);
        // White collar
        ctx.fillStyle = '#ffffff'; ctx.beginPath(); ctx.moveTo(px, pyDraw + 12); ctx.lineTo(px - 8, pyDraw + 8); ctx.lineTo(px + 8, pyDraw + 8); ctx.closePath(); ctx.fill();
        // Head & Face
        ctx.fillStyle = '#ffdbac'; ctx.beginPath(); ctx.arc(px, pyDraw - 4, 14, 0, Math.PI * 2); ctx.fill();
        // Hair (Short messy hair)
        ctx.fillStyle = '#222222'; ctx.beginPath(); ctx.arc(px, pyDraw - 8, 13, Math.PI * 0.8, Math.PI * 2.2); ctx.fill();
        // Signature Round Glasses
        ctx.strokeStyle = '#333333'; ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(px - 5, pyDraw - 5, 5, 0, Math.PI * 2);
        ctx.arc(px + 5, pyDraw - 5, 5, 0, Math.PI * 2);
        ctx.moveTo(px - 1, pyDraw - 5); ctx.lineTo(px + 1, pyDraw - 5);
        ctx.stroke();
        // Eyes inside glasses
        ctx.fillStyle = '#222222'; ctx.beginPath(); ctx.arc(px - 5, pyDraw - 5, 1.5, 0, Math.PI * 2); ctx.arc(px + 5, pyDraw - 5, 1.5, 0, Math.PI * 2); ctx.fill();
    }

    if (activePowerups.copter > 0) {
        ctx.fillStyle = '#ffcc00';
        ctx.fillRect(px - 12, pyDraw - 35, 24, 4);
        ctx.save();
        ctx.translate(px, pyDraw - 37);
        ctx.rotate(frame * 0.5);
        ctx.fillStyle = '#00ffaa';
        ctx.fillRect(-18, -2, 36, 4);
        ctx.restore();
    }

    if (activePowerups.shield > 0) {
        ctx.strokeStyle = 'rgba(0,255,150,0.7)'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(px, pyDraw + ph/2, 34, 0, Math.PI * 2); ctx.stroke();
    }
    ctx.restore();
}

function drawObstacle(o) {
    const x = o.x, y = o.y;
    if (o.type === 'train') {
        ctx.fillStyle = '#dd2222'; roundRect(x - o.w/2, y, o.w, o.h, 8);
        ctx.fillStyle = '#88ccff'; ctx.fillRect(x - o.w/2 + 8, y + 16, o.w - 16, 28);
        ctx.fillStyle = '#ffff00';
        ctx.beginPath(); ctx.arc(x - 14, y + o.h - 12, 5, 0, Math.PI*2); ctx.arc(x + 14, y + o.h - 12, 5, 0, Math.PI*2); ctx.fill();
    } else if (o.type === 'barrier') {
        ctx.fillStyle = '#ff6600'; roundRect(x - o.w/2, y, o.w, o.h, 6);
        ctx.fillStyle = '#fff'; ctx.font = 'bold 22px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('⚠', x, y + o.h/2 + 8);
    } else if (o.type === 'lowbarrier') {
        ctx.fillStyle = '#ff3300'; roundRect(x - o.w/2, y, o.w, o.h, 4);
        ctx.fillStyle = '#fff';
        for (let i = 0; i < 3; i++) ctx.fillRect(x - o.w/2 + 6 + i*15, y + 8, 8, o.h - 16);
    } else {
        ctx.fillStyle = '#8B4513'; roundRect(x - o.w/2, y, o.w, o.h, 6);
        ctx.fillStyle = '#ffcc00'; ctx.font = 'bold 18px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('📦', x, y + o.h/2 + 6);
    }
}

function drawCoin(c) {
    ctx.save(); ctx.translate(c.x, c.y); ctx.rotate(frame * 0.12);
    ctx.fillStyle = '#ffcc00'; ctx.beginPath(); ctx.arc(0, 0, c.r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#ff9900'; ctx.beginPath(); ctx.arc(0, 0, c.r * 0.65, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.font = 'bold 12px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('$', 0, 1); ctx.restore();
}

function drawPowerup(p) {
    const icons = { magnet: '🧲', copter: '🚁', scorex2: '✖2', shield: '🛡' };
    const colors = { magnet: '#00aaff', copter: '#00ffaa', scorex2: '#ffcc00', shield: '#00ff99' };
    ctx.fillStyle = colors[p.type] || '#fff';
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#fff'; ctx.font = '16px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(icons[p.type] || '?', p.x, p.y + 1);
}

function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h); ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath(); ctx.fill();
}

function showScreen(id) {
    ['menuScreen', 'charScreen', 'missionsScreen', 'settingsScreen', 'gameOverScreen', 'pauseScreen']
        .forEach(s => document.getElementById(s).classList.add('hidden'));
    if (id) {
        document.getElementById(id).classList.remove('hidden');
        if (id === 'charScreen') renderCharacters();
        if (id === 'missionsScreen') renderMissions();
        if (id === 'settingsScreen') {
            document.getElementById('soundToggle').checked = save.sound;
            document.getElementById('vibToggle').checked = save.vibration;
        }
    }
}

function updateMenuStats() {
    const currentHigh = save.highScores[save.difficulty] || 0;
    document.getElementById('menuHighScore').textContent = currentHigh;
    document.getElementById('menuCoins').textContent = save.coins;
}

function updateHud() {
    const currentHigh = save.highScores[save.difficulty] || 0;
    document.getElementById('hudScore').textContent = Math.floor(score);
    document.getElementById('hudCoins').textContent = runCoins;
    document.getElementById('hudHigh').textContent = Math.max(currentHigh, Math.floor(score));
}

function updatePowerupIcons() {
    document.getElementById('puMagnet').classList.toggle('active', activePowerups.magnet > 0);
    document.getElementById('puCopter').classList.toggle('active', activePowerups.copter > 0);
    document.getElementById('puScore').classList.toggle('active', activePowerups.scorex2 > 0);
    document.getElementById('puShield').classList.toggle('active', activePowerups.shield > 0);
}

function renderCharacters() {
    const list = document.getElementById('charList');
    list.innerHTML = '';
    CHARACTERS.forEach(char => {
        const selected = save.currentChar === char.id;
        const div = document.createElement('div');
        div.className = 'list-item' + (selected ? ' selected' : '');
        div.onclick = () => { save.currentChar = char.id; persist(); renderCharacters(); };
        div.innerHTML = `
            <div>
                <div style="font-weight:700;font-size:1.1rem;color:#00ffff;">${char.name}</div>
                <div style="font-size:0.85rem;color:#aaa;">${char.desc}</div>
            </div>
            <div>${selected ? '<span style="color:#00ff99;font-weight:bold;">Đang chọn ✓</span>' : '<button class="btn small" style="padding:6px 16px;min-width:auto;">Chọn</button>'}</div>
        `;
        list.appendChild(div);
    });
}

function renderMissions() {
    const list = document.getElementById('missionsList');
    list.innerHTML = '';
    save.missions.forEach(m => {
        const pct = Math.min(100, (m.progress / m.target) * 100);
        const done = m.progress >= m.target;
        const div = document.createElement('div');
        div.className = 'list-item';
        div.style.flexDirection = 'column';
        div.style.alignItems = 'flex-start';
        div.innerHTML = `
            <div style="width:100%;display:flex;justify-content:space-between;">
                <span style="font-weight:600;">${m.name}</span>
                <span style="color:#ffcc00;font-weight:700;">🪙 +${m.reward}</span>
            </div>
            <div style="width:100%;font-size:0.85rem;color:#aaa;margin-top:4px;">
                Tiến độ: ${Math.min(m.progress, m.target)} / ${m.target}
                ${done && !m.claimed ? `<button class="btn small" style="float:right;padding:2px 10px;" onclick="claimMission(\${m.id})">Nhận</button>` : (m.claimed ? ' ✓ Đã nhận' : '')}
            </div>
            <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
        `;
        list.appendChild(div);
    });
}

function claimMission(id) {
    const m = save.missions.find(x => x.id === id);
    if (m && m.progress >= m.target && !m.claimed) {
        m.claimed = true;
        save.coins += m.reward;
        persist();
        renderMissions();
        updateMenuStats();
    }
}

function toggleSound() {
    save.sound = document.getElementById('soundToggle').checked;
    if (!save.sound) stopBGM();
    else if (state === 'playing') startBGM();
    persist();
}

function loop() {
    if (state === 'playing') {
        update(); draw();
        requestAnimationFrame(loop);
    } else if (state === 'paused') {
        draw();
    }
}

function resize() {
    const maxW = Math.min(window.innerWidth, 480);
    const maxH = window.innerHeight;
    const ratio = 480 / 720;
    let cw = maxW, ch = maxW / ratio;
    if (ch > maxH) { ch = maxH; cw = ch * ratio; }
    canvas.style.width = cw + 'px';
    canvas.style.height = ch + 'px';
}
window.addEventListener('resize', resize);
resize();

loadSave();
showScreen('menuScreen');
draw();
</script>
</body>
</html>
"""

components.html(GAME_HTML, height=780, scrolling=False)