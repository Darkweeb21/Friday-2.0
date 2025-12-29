import { motion } from 'motion/react';

interface AICoreOrbProps {
  state: 'idle' | 'listening' | 'speaking' | 'typing' | 'pulse';
}

export function AICoreOrb({ state }: AICoreOrbProps) {
  // Animation variants for different states
  const getAnimationProps = () => {
    switch (state) {
      case 'typing':
        // Subtle contraction and brightness increase while user types
        return {
          scale: [1, 0.92, 0.92],
          opacity: [0.18, 0.28, 0.28],
        };
      case 'pulse':
        // Single gentle pulse on message send
        return {
          scale: [1, 1.15, 1],
          opacity: [0.18, 0.35, 0.18],
        };
      case 'listening':
        // Slight expansion and brightness when mic is active
        return {
          scale: [1, 1.08, 1],
          opacity: [0.2, 0.3, 0.2],
        };
      case 'speaking':
        // Calm rhythmic pulsing while FRIDAY responds
        return {
          scale: [1, 1.06, 1.03, 1],
          opacity: [0.18, 0.28, 0.22, 0.18],
        };
      case 'idle':
      default:
        // Slow breathing glow
        return {
          scale: [1, 1.04, 1],
          opacity: [0.15, 0.22, 0.15],
        };
    }
  };

  const animationProps = getAnimationProps();
  
  // Duration based on state
  const getDuration = () => {
    switch (state) {
      case 'pulse':
        return 1.2; // Quick single pulse
      case 'typing':
        return 0.8; // Fast transition to contracted state
      case 'speaking':
        return 2.5;
      case 'listening':
        return 3.5;
      case 'idle':
      default:
        return 5;
    }
  };

  const duration = getDuration();
  const repeat = state === 'pulse' || state === 'typing' ? 0 : Infinity;

  return (
    <div className="absolute inset-0 flex items-center justify-center pointer-events-none overflow-hidden">
      {/* Main orb container */}
      <motion.div
        className="relative"
        animate={animationProps}
        transition={{
          duration,
          repeat,
          ease: state === 'pulse' ? 'easeOut' : 'easeInOut',
        }}
      >
        {/* Outer glow layer - stronger presence */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(59, 130, 246, 0.22) 0%, rgba(34, 211, 238, 0.12) 30%, rgba(59, 130, 246, 0.05) 50%, transparent 70%)',
            filter: 'blur(50px)',
          }}
        />

        {/* Middle glow layer - increased visibility */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(96, 165, 250, 0.28) 0%, rgba(59, 130, 246, 0.18) 40%, rgba(37, 99, 235, 0.08) 65%, transparent 75%)',
            filter: 'blur(35px)',
          }}
        />

        {/* Core orb - stronger inner glow */}
        <div
          className="relative w-[200px] h-[200px] rounded-full"
          style={{
            background: 'radial-gradient(circle at 35% 35%, rgba(147, 197, 253, 0.38) 0%, rgba(59, 130, 246, 0.28) 30%, rgba(37, 99, 235, 0.18) 60%, rgba(30, 64, 175, 0.08) 85%, transparent 100%)',
            filter: 'blur(18px)',
          }}
        />

        {/* Soft edge definition */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[180px] h-[180px] rounded-full"
          style={{
            background: 'radial-gradient(circle, transparent 65%, rgba(59, 130, 246, 0.25) 75%, rgba(96, 165, 250, 0.15) 85%, transparent 95%)',
            filter: 'blur(8px)',
          }}
        />

        {/* Inner core highlight - brighter center */}
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[100px] h-[100px] rounded-full"
          style={{
            background: 'radial-gradient(circle, rgba(165, 180, 252, 0.45) 0%, rgba(139, 92, 246, 0.25) 50%, transparent 100%)',
            filter: 'blur(12px)',
          }}
        />

        {/* Subtle accent layer - slow rotation */}
        <motion.div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[280px] h-[280px] rounded-full"
          style={{
            background: 'radial-gradient(circle, transparent 40%, rgba(34, 211, 238, 0.12) 60%, transparent 80%)',
            filter: 'blur(20px)',
          }}
          animate={{
            rotate: [0, 360],
          }}
          transition={{
            duration: 40,
            repeat: Infinity,
            ease: 'linear',
          }}
        />
      </motion.div>
    </div>
  );
}