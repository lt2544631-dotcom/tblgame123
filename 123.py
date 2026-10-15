<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Flappy Dragon - Pixel Art Edition</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');
        
        body {
            font-family: 'Press Start 2P', cursive, monospace;
            background-color: #1a1a2e;
            touch-action: manipulation;
            user-select: none;
            -webkit-user-select: none;
        }

        #game-container {
            position: relative;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            border: 4px solid #000;
            border-radius: 12px;
            overflow: hidden;
        }

        canvas {
            display: block;
            image-rendering: pixelated;
            image-rendering: crisp-edges;
        }

        /* Custom Pixel Button Styles */
        .pixel-btn {
            background-color: #e67e22;
            box-shadow: inset -4px -4px 0px 0px #a3520e, inset 4px 4px 0px 0px #f39c12;
            border: 3px solid #000;
            color: white;
            text-shadow: 2px 2px #000;
            transition: all 0.1s ease;
        }

        .pixel-btn:active, .pixel-btn.active {
            background-color: #27ae60;
            box-shadow: inset 4px 4px 0px 0px #1e8449;
            transform: translateY(2px);
        }

        .pixel-box {
            background-color: #ded895;
            border: 4px solid #543847;
            box-shadow: inset -4px -4px 0px 0px #c3b96d, inset 4px 4px 0px 0px #fff;
            color: #543847;
        }
    </style>
</head>
<body class="min-h-screen flex flex-col items-center justify-center p-2 sm:p-4 text-white select-none">

    <!-- Audio Element for King Von - No Flaws -->
    <audio id="bg-music" loop preload="auto">
        <!-- King Von - No Flaws Stream Link with fallback -->
        <source src="https://ia801503.us.archive.org/15/items/king-von-no-flaws/King%20Von%20-%20No%20Flaws.mp3" type="audio/mpeg">
        <source src="https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/Trio_Targoviste/Live_at_WFMU/Trio_Targoviste_-_03_-_No_Flaws.mp3" type="audio/mpeg">
    </audio>

    <!-- Header / Title -->
    <div class="text-center mb-2">
        <h1 class="text-xl sm:text-2xl font-bold tracking-wider text-amber-400 drop-shadow-[0_4px_0_#000] flex items-center justify-center gap-2">
            🐲 FLAPPY DRAGON
        </h1>
        <p class="text-[10px] text-gray-400 mt-1">Chạm màn hình hoặc ấn [SPACE] để bay</p>
    </div>

    <!-- Game Viewport Container -->
    <div id="game-container" class="relative w-full max-w-[400px] h-[600px] bg-sky-300">
        <!-- Canvas Game Loop -->
        <canvas id="gameCanvas" width="360" height="640" class="w-full h-full"></canvas>

        <!-- Top Bar Audio Control Toggle -->
        <div class="absolute top-3 right-3 z-30">
            <button id="music-toggle-btn" class="pixel-btn text-[10px] px-2 py-1 flex items-center gap-1 cursor-pointer">
                <span id="music-icon">🎵</span> <span id="music-status">BẬT</span>
            </button>
        </div>

        <!-- Start Screen Overlay -->
        <div id="start-screen" class="absolute inset-0 flex flex-col items-center justify-between p-6 pointer-events-auto z-10 bg-black/20">
            <div class="mt-8 text-center animate-bounce">
                <div class="pixel-box px-4 py-3 rounded-lg text-xs font-bold text-amber-900 border-2">
                    NHẤN HOẶC [SPACE]<br>ĐỂ BẮT ĐẦU!
                </div>
            </div>

            <!-- Mode Selector Box -->
            <div class="pixel-box w-full p-4 rounded-lg text-center flex flex-col items-center gap-2 border-3">
                <p class="text-xs font-bold text-amber-900 mb-1">CHỌN CHẾ ĐỘ CHƠI:</p>
                <div class="grid grid-cols-3 gap-2 w-full">
                    <button data-mode="easy" class="mode-btn pixel-btn text-[10px] py-2 px-1 rounded cursor-pointer">DỄ</button>
                    <button data-mode="normal" class="mode-btn pixel-btn active text-[10px] py-2 px-1 rounded cursor-pointer">THƯỜNG</button>
                    <button data-mode="hard" class="mode-btn pixel-btn text-[10px] py-2 px-1 rounded cursor-pointer">KHÓ</button>
                </div>
                <div class="text-[9px] text-amber-800 mt-1 font-bold">
                    🎶 Nhạc nền: <span class="text-red-700">No Flaws - King Von</span>
                </div>
            </div>

            <div class="mb-4 text-center text-[10px] text-white drop-shadow-[0_2px_2px_#000]">
                <p>Né tránh các ống cống xanh</p>
                <p class="mt-1 text-amber-300">🔥 Rồng Nhỏ Phiêu Lưu 🔥</p>
            </div>
        </div>

        <!-- Game Over Modal Overlay -->
        <div id="game-over-screen" class="absolute inset-0 bg-black/70 flex flex-col items-center justify-center p-6 hidden z-20">
            <div class="pixel-box w-full p-5 rounded-lg text-center flex flex-col items-center gap-3 border-4">
                <h2 class="text-lg font-bold text-red-600 drop-shadow-[0_2px_0_#000]">GAME OVER</h2>
                
                <div class="w-full bg-[#c3b96d] p-3 rounded border-2 border-[#543847] flex flex-col gap-2">
                    <div class="flex justify-between items-center text-[11px]">
                        <span>CHẾ ĐỘ:</span>
                        <span id="display-mode" class="text-xs font-bold text-amber-900">BÌNH THƯỜNG</span>
                    </div>
                    <div class="flex justify-between items-center text-[11px] border-t border-[#a89e52] pt-1">
                        <span>ĐIỂM SỐ:</span>
                        <span id="final-score" class="text-base font-bold text-amber-900">0</span>
                    </div>
                    <div class="flex justify-between items-center text-[11px] border-t border-[#a89e52] pt-1">
                        <span>KỶ LỤC:</span>
                        <span id="best-score" class="text-base font-bold text-amber-900">0</span>
                    </div>
                </div>

                <div id="new-high-score" class="hidden text-[10px] text-red-600 font-bold animate-pulse">
                    🎉 KỶ LỤC MỚI! 🎉
                </div>

                <!-- Mode Switcher in Game Over Screen -->
                <div class="grid grid-cols-3 gap-1 w-full mt-1">
                    <button data-mode="easy" class="mode-btn pixel-btn text-[9px] py-1.5 px-1 rounded cursor-pointer">DỄ</button>
                    <button data-mode="normal" class="mode-btn pixel-btn active text-[9px] py-1.5 px-1 rounded cursor-pointer">THƯỜNG</button>
                    <button data-mode="hard" class="mode-btn pixel-btn text-[9px] py-1.5 px-1 rounded cursor-pointer">KHÓ</button>
                </div>

                <button id="restart-btn" class="pixel-btn w-full py-2.5 text-xs font-bold rounded cursor-pointer mt-1">
                    CHƠI LẠI
                </button>
            </div>
        </div>
    </div>

    <!-- Instructions / Streamlit Guide Toggle -->
    <div class="mt-3 max-w-[400px] w-full text-center">
        <button id="toggle-code-btn" class="text-xs text-amber-400 underline hover:text-amber-300 cursor-pointer">
            👉 Xem cách nhúng vào Streamlit & GitHub
        </button>
        <div id="code-instructions" class="hidden mt-3 p-3 bg-gray-900 rounded-lg border border-gray-700 text-left text-xs text-gray-300 space-y-2">
            <p class="font-bold text-amber-400">Cách nhúng vào Streamlit:</p>
            <ol class="list-decimal list-inside space-y-1 text-[11px]">
                <li>Lưu mã nguồn HTML này thành file <code class="text-green-400">flappy.html</code></li>
                <li>Trong file Streamlit <code class="text-green-400">app.py</code>, sử dụng mã sau:</li>
            </ol>
            <pre class="bg-black p-2 rounded text-[10px] text-green-400 overflow-x-auto">import streamlit as st

st.set_page_config(page_title="Flappy Dragon", layout="centered")
st.title("🐲 Flappy Dragon")

with open("flappy.html", "r", encoding="utf-8") as f:
    html_code = f.read()

st.components.v1.html(html_code, height=720, scrolling=False)</pre>
        </div>
    </div>

    <!-- Game Logic Script -->
    <script>
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');
        const bgMusic = document.getElementById('bg-music');
        
        // UI Elements
        const startScreen = document.getElementById('start-screen');
        const gameOverScreen = document.getElementById('game-over-screen');
        const finalScoreEl = document.getElementById('final-score');
        const bestScoreEl = document.getElementById('best-score');
        const displayModeEl = document.getElementById('display-mode');
        const newHighScoreEl = document.getElementById('new-high-score');
        const restartBtn = document.getElementById('restart-btn');
        const toggleCodeBtn = document.getElementById('toggle-code-btn');
        const codeInstructions = document.getElementById('code-instructions');
        const musicToggleBtn = document.getElementById('music-toggle-btn');
        const musicIcon = document.getElementById('music-icon');
        const musicStatus = document.getElementById('music-status');
        const modeBtns = document.querySelectorAll('.mode-btn');

        // Game Constants & Difficulty Configurations
        const CANVAS_WIDTH = 360;
        const CANVAS_HEIGHT = 640;
        const GROUND_HEIGHT = 90;

        const DIFFICULTY_SETTINGS = {
            easy: {
                name: "DỄ",
                gravity: 0.35,
                jump: -7.5,
                pipeSpeed: 1.8,
                pipeGap: 175,
                spawnInterval: 110
            },
            normal: {
                name: "THƯỜNG",
                gravity: 0.45,
                jump: -8.5,
                pipeSpeed: 2.5,
                pipeGap: 135,
                spawnInterval: 95
            },
            hard: {
                name: "KHÓ",
                gravity: 0.55,
                jump: -9.5,
                pipeSpeed: 3.5,
                pipeGap: 105,
                spawnInterval: 80
            }
        };

        let currentDifficulty = 'normal';
        let musicEnabled = true;

        // Sound Effects Synthesizer (Web Audio API)
        class SoundEffects {
            constructor() {
                this.ctx = null;
            }

            initCtx() {
                if (!this.ctx) {
                    this.ctx = new (window.AudioContext || window.webkitAudioContext)();
                }
            }
            
            playFlap() {
                if (!musicEnabled) return;
                this.initCtx();
                if (this.ctx.state === 'suspended') this.ctx.resume();
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(400, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(800, this.ctx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.2, this.ctx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.1);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.1);
            }

            playScore() {
                if (!musicEnabled) return;
                this.initCtx();
                if (this.ctx.state === 'suspended') this.ctx.resume();
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'square';
                osc.frequency.setValueAtTime(523.25, this.ctx.currentTime);
                osc.frequency.setValueAtTime(659.25, this.ctx.currentTime + 0.08);
                gain.gain.setValueAtTime(0.1, this.ctx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.2);
            }

            playHit() {
                if (!musicEnabled) return;
                this.initCtx();
                if (this.ctx.state === 'suspended') this.ctx.resume();
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sawtooth';
                osc.frequency.setValueAtTime(150, this.ctx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(40, this.ctx.currentTime + 0.2);
                gain.gain.setValueAtTime(0.3, this.ctx.currentTime);
                gain.gain.linearRampToValueAtTime(0.01, this.ctx.currentTime + 0.2);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start();
                osc.stop(this.ctx.currentTime + 0.2);
            }
        }

        const sounds = new SoundEffects();

        // Game State Variables
        let gameState = 'START'; // START, PLAYING, GAMEOVER
        let score = 0;
        let frameCount = 0;
        let groundOffset = 0;

        function getHighScore(mode) {
            return parseInt(localStorage.getItem(`flappy_dragon_highscore_${mode}`) || '0');
        }

        function setHighScore(mode, value) {
            localStorage.setItem(`flappy_dragon_highscore_${mode}`, value.toString());
        }

        // Dragon Object
        const dragon = {
            x: 70,
            y: 280,
            width: 38,
            height: 32,
            velocity: 0,
            rotation: 0,
            wingFrame: 0,
            wingTimer: 0,

            reset() {
                this.y = 280;
                this.velocity = 0;
                this.rotation = 0;
                this.wingFrame = 0;
            },

            flap() {
                const settings = DIFFICULTY_SETTINGS[currentDifficulty];
                this.velocity = settings.jump;
                sounds.playFlap();
            },

            update() {
                const settings = DIFFICULTY_SETTINGS[currentDifficulty];

                if (gameState === 'PLAYING') {
                    this.velocity += settings.gravity;
                    this.y += this.velocity;

                    // Rotation logic
                    if (this.velocity < 0) {
                        this.rotation = -0.35;
                    } else {
                        this.rotation += 0.04;
                        if (this.rotation > 0.7) this.rotation = 0.7;
                    }

                    // Wing animation timer
                    this.wingTimer++;
                    if (this.wingTimer % 6 === 0) {
                        this.wingFrame = (this.wingFrame + 1) % 3;
                    }

                    // Ground collision
                    if (this.y + this.height / 2 >= CANVAS_HEIGHT - GROUND_HEIGHT) {
                        this.y = CANVAS_HEIGHT - GROUND_HEIGHT - this.height / 2;
                        triggerGameOver();
                    }

                    // Ceiling collision
                    if (this.y - this.height / 2 <= 0) {
                        this.y = this.height / 2;
                        this.velocity = 0;
                    }
                } else if (gameState === 'START') {
                    // Hovering effect
                    this.y = 280 + Math.sin(frameCount * 0.08) * 8;
                    this.wingTimer++;
                    if (this.wingTimer % 8 === 0) {
                        this.wingFrame = (this.wingFrame + 1) % 3;
                    }
                }
            },

            draw() {
                ctx.save();
                ctx.translate(this.x, this.y);
                ctx.rotate(this.rotation);

                const p = 2; // Pixel scale unit

                // Body
                ctx.fillStyle = '#2ecc71';
                ctx.fillRect(-8 * p, -6 * p, 16 * p, 12 * p);
                ctx.fillRect(4 * p, -4 * p, 6 * p, 8 * p);

                // Shading
                ctx.fillStyle = '#27ae60';
                ctx.fillRect(-8 * p, 2 * p, 16 * p, 4 * p);

                // Yellow Belly
                ctx.fillStyle = '#f1c40f';
                ctx.fillRect(-4 * p, 0, 8 * p, 5 * p);

                // Red Spikes & Tail
                ctx.fillStyle = '#e74c3c';
                ctx.fillRect(-8 * p, -9 * p, 3 * p, 3 * p);
                ctx.fillRect(-3 * p, -9 * p, 3 * p, 3 * p);
                ctx.fillRect(-8 * p, 6 * p, 3 * p, 3 * p);

                // Eye
                ctx.fillStyle = '#ffffff';
                ctx.fillRect(4 * p, -5 * p, 4 * p, 4 * p);
                ctx.fillStyle = '#000000';
                ctx.fillRect(6 * p, -4 * p, 2 * p, 2 * p);

                // Flame particle on jump
                if (this.velocity < -2) {
                    ctx.fillStyle = '#f39c12';
                    ctx.fillRect(10 * p, -1 * p, 4 * p, 3 * p);
                    ctx.fillStyle = '#e74c3c';
                    ctx.fillRect(14 * p, 0 * p, 2 * p, 2 * p);
                }

                // Wings
                ctx.fillStyle = '#c0392b';
                if (this.wingFrame === 0) {
                    ctx.beginPath();
                    ctx.moveTo(-2 * p, -4 * p);
                    ctx.lineTo(-8 * p, -14 * p);
                    ctx.lineTo(2 * p, -10 * p);
                    ctx.closePath();
                    ctx.fill();
                    ctx.fillStyle = '#e74c3c';
                    ctx.fillRect(-6 * p, -11 * p, 4 * p, 4 * p);
                } else if (this.wingFrame === 1) {
                    ctx.fillRect(-10 * p, -4 * p, 8 * p, 4 * p);
                    ctx.fillStyle = '#e74c3c';
                    ctx.fillRect(-8 * p, -3 * p, 5 * p, 2 * p);
                } else {
                    ctx.beginPath();
                    ctx.moveTo(-2 * p, 0);
                    ctx.lineTo(-8 * p, 10 * p);
                    ctx.lineTo(2 * p, 6 * p);
                    ctx.closePath();
                    ctx.fill();
                }

                ctx.restore();
            }
        };

        // Pipe Management
        const pipes = [];

        class Pipe {
            constructor() {
                const settings = DIFFICULTY_SETTINGS[currentDifficulty];
                this.x = CANVAS_WIDTH;
                const minHeight = 50;
                const maxHeight = CANVAS_HEIGHT - GROUND_HEIGHT - settings.pipeGap - 50;
                this.topHeight = Math.floor(Math.random() * (maxHeight - minHeight + 1)) + minHeight;
                this.bottomY = this.topHeight + settings.pipeGap;
                this.bottomHeight = CANVAS_HEIGHT - GROUND_HEIGHT - this.bottomY;
                this.width = 54;
                this.passed = false;
            }

            update() {
                const settings = DIFFICULTY_SETTINGS[currentDifficulty];
                this.x -= settings.pipeSpeed;

                if (!this.passed && this.x + this.width < dragon.x) {
                    this.passed = true;
                    score++;
                    sounds.playScore();
                }
            }

            draw() {
                const pipeGreen = '#73bf2e';
                const pipeDarkGreen = '#558022';
                const pipeLightGreen = '#9ce659';
                const pipeBorder = '#000000';
                const capHeight = 24;
                const capOutset = 3;

                // --- TOP PIPE ---
                ctx.fillStyle = pipeGreen;
                ctx.fillRect(this.x, 0, this.width, this.topHeight);
                ctx.fillStyle = pipeLightGreen;
                ctx.fillRect(this.x + 4, 0, 6, this.topHeight);
                ctx.fillStyle = pipeDarkGreen;
                ctx.fillRect(this.x + this.width - 8, 0, 6, this.topHeight);
                ctx.strokeStyle = pipeBorder;
                ctx.lineWidth = 2;
                ctx.strokeRect(this.x, 0, this.width, this.topHeight);

                const capX = this.x - capOutset;
                const capW = this.width + capOutset * 2;
                const capY = this.topHeight - capHeight;
                ctx.fillStyle = pipeGreen;
                ctx.fillRect(capX, capY, capW, capHeight);
                ctx.fillStyle = pipeLightGreen;
                ctx.fillRect(capX + 4, capY, 6, capHeight);
                ctx.fillStyle = pipeDarkGreen;
                ctx.fillRect(capX + capW - 8, capY, 6, capHeight);
                ctx.strokeRect(capX, capY, capW, capHeight);

                // --- BOTTOM PIPE ---
                ctx.fillStyle = pipeGreen;
                ctx.fillRect(this.x, this.bottomY, this.width, this.bottomHeight);
                ctx.fillStyle = pipeLightGreen;
                ctx.fillRect(this.x + 4, this.bottomY, 6, this.bottomHeight);
                ctx.fillStyle = pipeDarkGreen;
                ctx.fillRect(this.x + this.width - 8, this.bottomY, 6, this.bottomHeight);
                ctx.strokeRect(this.x, this.bottomY, this.width, this.bottomHeight);

                ctx.fillStyle = pipeGreen;
                ctx.fillRect(capX, this.bottomY, capW, capHeight);
                ctx.fillStyle = pipeLightGreen;
                ctx.fillRect(capX + 4, capY, 6, capHeight);
                ctx.fillStyle = pipeDarkGreen;
                ctx.fillRect(capX + capW - 8, capY, 6, capHeight);
                ctx.strokeRect(capX, this.bottomY, capW, capHeight);
            }

            collidesWith(dragonObj) {
                const padding = 6;
                const dLeft = dragonObj.x - dragonObj.width / 2 + padding;
                const dRight = dragonObj.x + dragonObj.width / 2 - padding;
                const dTop = dragonObj.y - dragonObj.height / 2 + padding;
                const dBottom = dragonObj.y + dragonObj.height / 2 - padding;

                const pipeLeft = this.x;
                const pipeRight = this.x + this.width;

                if (dRight > pipeLeft && dLeft < pipeRight && dTop < this.topHeight) {
                    return true;
                }
                if (dRight > pipeLeft && dLeft < pipeRight && dBottom > this.bottomY) {
                    return true;
                }
                return false;
            }
        }

        // Draw Background
        function drawBackground() {
            // Sky
            ctx.fillStyle = '#4ec0ca';
            ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

            // Clouds
            ctx.fillStyle = '#ffffff';
            drawCloud(40 - (frameCount * 0.2) % (CANVAS_WIDTH + 80), 120);
            drawCloud(220 - (frameCount * 0.2) % (CANVAS_WIDTH + 80), 80);

            // City
            const cityY = CANVAS_HEIGHT - GROUND_HEIGHT - 60;
            ctx.fillStyle = '#83d3b0';
            for (let i = 0; i < CANVAS_WIDTH; i += 30) {
                const h = 30 + Math.sin(i * 12) * 20;
                ctx.fillRect(i, cityY + (60 - h), 22, h);
                ctx.fillStyle = '#bdf2d5';
                ctx.fillRect(i + 4, cityY + (60 - h) + 6, 4, 4);
                ctx.fillRect(i + 12, cityY + (60 - h) + 6, 4, 4);
                ctx.fillStyle = '#83d3b0';
            }

            // Bushes
            const bushY = CANVAS_HEIGHT - GROUND_HEIGHT - 22;
            ctx.fillStyle = '#5ee183';
            ctx.fillRect(0, bushY, CANVAS_WIDTH, 22);
            ctx.fillStyle = '#25b152';
            for (let i = 0; i < CANVAS_WIDTH; i += 20) {
                ctx.beginPath();
                ctx.arc(i + 10, bushY, 12, 0, Math.PI, true);
                ctx.fill();
            }

            // Ground
            const groundY = CANVAS_HEIGHT - GROUND_HEIGHT;
            ctx.fillStyle = '#73bf2e';
            ctx.fillRect(0, groundY, CANVAS_WIDTH, 14);
            ctx.fillStyle = '#558022';
            ctx.fillRect(0, groundY + 12, CANVAS_WIDTH, 3);

            ctx.fillStyle = '#ded895';
            ctx.fillRect(0, groundY + 15, CANVAS_WIDTH, GROUND_HEIGHT - 15);

            const settings = DIFFICULTY_SETTINGS[currentDifficulty];
            if (gameState === 'PLAYING' || gameState === 'START') {
                groundOffset = (groundOffset + settings.pipeSpeed) % 18;
            }
            ctx.fillStyle = '#c3b96d';
            ctx.strokeStyle = '#9e9447';
            ctx.lineWidth = 2;
            for (let x = -20; x < CANVAS_WIDTH + 20; x += 18) {
                ctx.beginPath();
                ctx.moveTo(x - groundOffset, groundY + 15);
                ctx.lineTo(x - groundOffset - 8, groundY + GROUND_HEIGHT);
                ctx.stroke();
            }

            ctx.fillStyle = '#000000';
            ctx.fillRect(0, groundY, CANVAS_WIDTH, 2);
        }

        function drawCloud(cx, cy) {
            ctx.beginPath();
            ctx.arc(cx, cy, 16, 0, Math.PI * 2);
            ctx.arc(cx + 14, cy - 8, 18, 0, Math.PI * 2);
            ctx.arc(cx + 32, cy, 14, 0, Math.PI * 2);
            ctx.closePath();
            ctx.fill();
        }

        // Draw Score
        function drawScore() {
            if (gameState === 'PLAYING') {
                ctx.fillStyle = '#ffffff';
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 4;
                ctx.font = '26px "Press Start 2P", monospace';
                ctx.textAlign = 'center';
                ctx.strokeText(score.toString(), CANVAS_WIDTH / 2, 70);
                ctx.fillText(score.toString(), CANVAS_WIDTH / 2, 70);

                // Mode Indicator badge
                ctx.font = '10px "Press Start 2P", monospace';
                ctx.fillStyle = '#f1c40f';
                ctx.fillText(DIFFICULTY_SETTINGS[currentDifficulty].name, CANVAS_WIDTH / 2, 92);
            }
        }

        // Audio Handler
        function playBackgroundAudio() {
            if (musicEnabled) {
                bgMusic.play().catch(() => {
                    // Browser policy silent catch
                });
            }
        }

        function stopBackgroundAudio() {
            bgMusic.pause();
        }

        // Handle Flap / Action
        function handleAction() {
            if (gameState === 'START') {
                gameState = 'PLAYING';
                startScreen.classList.add('hidden');
                playBackgroundAudio();
                dragon.flap();
            } else if (gameState === 'PLAYING') {
                dragon.flap();
            }
        }

        function triggerGameOver() {
            if (gameState === 'GAMEOVER') return;
            
            gameState = 'GAMEOVER';
            sounds.playHit();
            stopBackgroundAudio();

            const currentHigh = getHighScore(currentDifficulty);
            let newBest = false;
            if (score > currentHigh) {
                setHighScore(currentDifficulty, score);
                newBest = true;
            }

            finalScoreEl.textContent = score;
            bestScoreEl.textContent = getHighScore(currentDifficulty);
            displayModeEl.textContent = DIFFICULTY_SETTINGS[currentDifficulty].name;

            if (newBest) {
                newHighScoreEl.classList.remove('hidden');
            } else {
                newHighScoreEl.classList.add('hidden');
            }

            gameOverScreen.classList.remove('hidden');
        }

        function restartGame() {
            score = 0;
            pipes.length = 0;
            frameCount = 0;
            dragon.reset();
            gameState = 'START';
            gameOverScreen.classList.add('hidden');
            startScreen.classList.remove('hidden');
        }

        function setDifficulty(mode) {
            currentDifficulty = mode;
            modeBtns.forEach(btn => {
                if (btn.dataset.mode === mode) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            });
        }

        // Main Loop
        function gameLoop() {
            frameCount++;

            dragon.update();

            if (gameState === 'PLAYING') {
                const settings = DIFFICULTY_SETTINGS[currentDifficulty];
                if (frameCount % settings.spawnInterval === 0) {
                    pipes.push(new Pipe());
                }

                for (let i = pipes.length - 1; i >= 0; i--) {
                    pipes[i].update();

                    if (pipes[i].collidesWith(dragon)) {
                        triggerGameOver();
                    }

                    if (pipes[i].x + pipes[i].width < -100) {
                        pipes.splice(i, 1);
                    }
                }
            }

            ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
            drawBackground();

            for (let pipe of pipes) {
                pipe.draw();
            }

            dragon.draw();
            drawScore();

            requestAnimationFrame(gameLoop);
        }

        // Controls & Events
        window.addEventListener('keydown', (e) => {
            if (e.code === 'Space') {
                e.preventDefault();
                handleAction();
            }
        });

        canvas.addEventListener('pointerdown', (e) => {
            e.preventDefault();
            handleAction();
        });

        restartBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            restartGame();
        });

        toggleCodeBtn.addEventListener('click', () => {
            codeInstructions.classList.toggle('hidden');
        });

        // Difficulty Selection
        modeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                setDifficulty(btn.dataset.mode);
            });
        });

        // Music Toggle
        musicToggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            musicEnabled = !musicEnabled;
            if (musicEnabled) {
                musicIcon.textContent = "🎵";
                musicStatus.textContent = "BẬT";
                if (gameState === 'PLAYING') playBackgroundAudio();
            } else {
                musicIcon.textContent = "🔇";
                musicStatus.textContent = "TẮT";
                stopBackgroundAudio();
            }
        });

        window.onload = () => {
            gameLoop();
        };
    </script>
</body>
</html>