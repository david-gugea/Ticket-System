<template>
  <div>
    <canvas ref="canvas" class="particle-canvas" @mousemove="handleMouseMove"></canvas>
    <div class="center-card">
      <transition name="fade">
        <img ref="logo" class="logo" alt="Logo" src="../assets/logo.png" v-if="showLogo">
      </transition>
      <router-link to="/login" class="btn btn-outline-light btn-lg px-5" style="margin-top: 10px;">Login</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      particles: [],
      canvas: null,
      ctx: null,
      particleCount: 300,
      mouse: {
        x: 0,
        y: 0,
      },
      showLogo: false,
    };
  },
  mounted() {
    this.initializeCanvas();
    this.createParticles();
    setTimeout(() => {
      this.showLogo = true;
      this.startLogoAnimation();
      this.animate();
    }, 1000);
  },
  methods: {
    initializeCanvas() {
      this.canvas = this.$refs.canvas;
      this.ctx = this.canvas.getContext('2d');
      this.resizeCanvas();
      window.addEventListener('resize', this.resizeCanvas);
    },
    resizeCanvas() {
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
      this.createParticles();
    },
    createParticles() {
      this.particles = [];
      for (let i = 0; i < this.particleCount; i++) {
        this.particles.push({
          x: Math.random() * this.canvas.width,
          y: Math.random() * this.canvas.height,
          radius: Math.random() * 3 + 1,
          color: `rgba(165, 224, 218, ${Math.random()})`,
          speedX: Math.random() - 0.5,
          speedY: Math.random() - 0.5,
        });
      }
    },
    startLogoAnimation() {
      this.$nextTick(() => {
        const logo = this.$refs.logo;
        if (logo) {
          logo.style.animation = 'fadeIn 1s ease-in-out';
        }
      });
    },
    animate() {
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
      this.particles.forEach((particle) => {
        this.drawParticle(particle);
        this.updateParticle(particle);
      });
      requestAnimationFrame(this.animate);
    },
    drawParticle(particle) {
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = particle.color;
      this.ctx.fill();
    },
    updateParticle(particle) {
      const dx = this.mouse.x - particle.x;
      const dy = this.mouse.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < 100) {
        const angle = Math.atan2(dy, dx);
        particle.speedX = Math.cos(angle) * 2;
        particle.speedY = Math.sin(angle) * 2;
      }

      particle.x += particle.speedX;
      particle.y += particle.speedY;

      if (
        particle.x + particle.radius > this.canvas.width ||
        particle.x - particle.radius < 0
      ) {
        particle.speedX = -particle.speedX;
      }

      if (
        particle.y + particle.radius > this.canvas.height ||
        particle.y - particle.radius < 0
      ) {
        particle.speedY = -particle.speedY;
      }
    },
    handleMouseMove(event) {
      this.mouse.x = event.clientX;
      this.mouse.y = event.clientY;
    },
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.resizeCanvas);
  },
};
</script>

<style scoped>
.particle-canvas {
  display: block;
  background: radial-gradient(closest-corner, #1d2020, #000000);
}

.center-card {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;
  text-align: center;
}

.logo {
  width: 100%; 
  height: auto;
}

/* CSS animation for logo fade-in */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 1s;
}

.fade-enter, .fade-leave-to {
  opacity: 1;
}
</style>
