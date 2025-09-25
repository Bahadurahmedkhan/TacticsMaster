import React from 'react';
import { ClipboardCheck, Users, Zap, ArrowRight } from 'lucide-react';

// Custom hook to detect when an element is in view
const useInView = (options) => {
    const [inView, setInView] = React.useState(false);
    const ref = React.useRef(null);

    React.useEffect(() => {
        const observer = new IntersectionObserver(([entry]) => {
            if (entry.isIntersecting) {
                setInView(true);
                observer.unobserve(entry.target);
            }
        }, options);

        const currentRef = ref.current;
        if (currentRef) {
            observer.observe(currentRef);
        }

        return () => {
            if (currentRef) {
                observer.unobserve(currentRef);
            }
        };
    }, [ref, options]);

    return [ref, inView];
};

const HolographicBlueprintAnimation = () => {
    // A metaphorical animation of a strategic blueprint coming to life.
    return (
        <div className="w-full max-w-3xl mx-auto h-64 md:h-96 mb-4 svg-container relative">
            <svg viewBox="0 0 600 250" className="w-full h-full" preserveAspectRatio="xMidYMid meet">
                <defs>
                    <linearGradient id="scan-line-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgba(0, 255, 255, 0)" />
                        <stop offset="50%" stopColor="rgba(0, 255, 255, 0.7)" />
                        <stop offset="100%" stopColor="rgba(0, 255, 255, 0)" />
                    </linearGradient>
                    <linearGradient id="title-gradient-blueprint" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="#00f2ff" />
                        <stop offset="100%" stopColor="#ffffff" />
                    </linearGradient>
                    <filter id="glow-filter-blueprint">
                        <feGaussianBlur stdDeviation="3" result="coloredBlur" />
                        <feMerge>
                            <feMergeNode in="coloredBlur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                {/* Scanning line that reveals the grid */}
                <rect className="scan-line" x="-10" y="0" width="10" height="250" fill="url(#scan-line-gradient)" />

                {/* Blueprint Elements (initially hidden) */}
                <g className="blueprint" opacity="0">
                    {/* Field Outline */}
                    <ellipse cx="300" cy="125" rx="250" ry="100" stroke="#00f2ff" strokeWidth="1" fill="none" className="field-line" />
                    
                    {/* Inner Pitch */}
                    <rect x="280" y="25" width="40" height="200" stroke="#00f2ff" strokeWidth="0.5" fill="rgba(0, 255, 255, 0.05)" className="field-line" />

                    {/* Stumps */}
                    <path d="M 290 40 L 290 50 M 300 40 L 300 50 M 310 40 L 310 50" stroke="#fff" strokeWidth="1.5" className="field-element" />
                    <path d="M 290 200 L 290 210 M 300 200 L 300 210 M 310 200 L 310 210" stroke="#fff" strokeWidth="1.5" className="field-element" />

                    {/* Strategic Markers & Arrows */}
                    <circle cx="200" cy="125" r="4" fill="none" stroke="#ff4d4d" strokeWidth="2" className="strategic-marker" />
                    <path d="M 200 125 C 250 100, 350 100, 400 125" fill="none" stroke="#ff4d4d" strokeWidth="1" strokeDasharray="3 3" className="strategic-path" />
                    <polygon points="395,120 400,125 395,130" fill="#ff4d4d" className="strategic-marker" />

                    {/* AI Core */}
                    <g className="ai-core" transform="translate(300, 125)">
                        <circle r="10" fill="none" stroke="#00f2ff" strokeWidth="1.5" />
                        <path d="M 0 -10 L 0 10 M -10 0 L 10 0" stroke="#00f2ff" strokeWidth="0.5" />
                    </g>
                </g>

                {/* Title construction lines */}
                <path className="title-line-1" d="M 50 125 L 280 125" stroke="#00f2ff" strokeWidth="1.5" />
                <path className="title-line-2" d="M 550 125 L 320 125" stroke="#00f2ff" strokeWidth="1.5" />

                {/* Final Title */}
                <text x="300" y="135" fontFamily="sans-serif" fontSize="50" fontWeight="bold" textAnchor="middle" fill="url(#title-gradient-blueprint)" className="title-text" opacity="0" filter="url(#glow-filter-blueprint)">
                    Tactics Master
                </text>
            </svg>
        </div>
    );
};

const WelcomePage = ({ onGetStarted }) => {
    React.useEffect(() => {
        const handleMouseMove = (e) => {
            document.documentElement.style.setProperty('--mouse-x', `${e.clientX}px`);
            document.documentElement.style.setProperty('--mouse-y', `${e.clientY}px`);
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    const features = [
        { icon: <ClipboardCheck size={32} className="text-cyan-300" />, title: "Data-Driven Strategies", description: "Leverage advanced analytics to generate optimal team strategies and game plans based on historical data." },
        { icon: <Users size={32} className="text-cyan-300" />, title: "Player Matchup Analysis", description: "Instantly analyze head-to-head stats between batsmen and bowlers to exploit weaknesses." },
        { icon: <Zap size={32} className="text-cyan-300" />, title: "Real-Time Insights", description: "Get live recommendations and tactical adjustments during the match to respond effectively." },
    ];

    const FeatureCard = ({ icon, title, description, index }) => {
        const [ref, inView] = useInView({ threshold: 0.1 });
        return (
            <div ref={ref} style={{ animationDelay: `${index * 150}ms` }} className={`feature-card border border-cyan-300/20 rounded-xl p-6 transition-all duration-500 ${inView ? 'animate-fly-in' : 'opacity-0 translate-y-10'}`}>
                <div className="mb-4">{icon}</div>
                <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
                <p className="text-gray-400">{description}</p>
            </div>
        );
    };

    return (
        <>
            <style>{`
                :root { --mouse-x: -1000px; --mouse-y: -1000px; }
                .bg-grid { background-image: linear-gradient(rgba(0, 255, 255, 0.05) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 255, 0.05) 1px, transparent 1px); background-size: 2rem 2rem; }
                .mouse-glow { position: fixed; top: 0; left: 0; width: 500px; height: 500px; background: radial-gradient(circle at center, rgba(0, 255, 255, 0.08) 0%, rgba(0, 255, 255, 0) 60%); border-radius: 50%; pointer-events: none; transform: translate(calc(var(--mouse-x) - 50%), calc(var(--mouse-y) - 50%)); transition: transform 0.1s ease-out; z-index: 5; }
                .feature-card { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
                .feature-card:hover { transform: translateY(-5px) scale(1.02); border-color: rgba(0, 255, 255, 0.4); box-shadow: 0 0 20px rgba(0, 255, 255, 0.1); }
                
                /* Animations */
                @keyframes slow-fade-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes fly-in { from { opacity: 0; transform: translateY(50px); } to { opacity: 1; transform: translateY(0); } }
                @keyframes pulse-glow { 0%, 100% { opacity: 0.1; } 50% { opacity: 0.2; } }
                .pulse-glow-1 { animation: pulse-glow 9s infinite ease-in-out; }
                .pulse-glow-2 { animation: pulse-glow 7s infinite ease-in-out; }

                /* -- Holographic Blueprint Animation -- */

                /* 1. Scan line moves across */
                @keyframes scan {
                    0% { transform: translateX(0); }
                    100% { transform: translateX(620px); }
                }
                .scan-line { animation: scan 1.5s cubic-bezier(0.6, 0.04, 0.98, 0.335) forwards; }
                
                /* 2. Blueprint materializes after scan */
                @keyframes materialize-blueprint { to { opacity: 1; } }
                .blueprint { animation: materialize-blueprint 0.5s ease-out forwards 1s; }

                /* 3. Field lines are drawn */
                @keyframes draw-line { from { stroke-dashoffset: 1000; } to { stroke-dashoffset: 0; } }
                .field-line { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw-line 2s ease-out forwards 1.5s; }
                .field-element { opacity: 0; animation: slow-fade-in 1s forwards 2.5s; }

                /* 4. AI Core and strategic paths activate */
                @keyframes core-pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.2); }
                }
                .ai-core { transform-origin: center; animation: core-pulse 2s infinite ease-in-out 3s; }
                .strategic-path { stroke-dasharray: 200; stroke-dashoffset: 200; animation: draw-line 1.5s ease-out forwards 3.2s; }
                .strategic-marker { opacity: 0; animation: slow-fade-in 0.5s forwards 3s; }

                /* 5. Construction lines form the title space */
                @keyframes converge-lines { from { transform: scaleX(1); } to { transform: scaleX(0); } }
                .title-line-1 { transform-origin: left; animation: converge-lines 1s ease-in-out forwards 4s; }
                .title-line-2 { transform-origin: right; animation: converge-lines 1s ease-in-out forwards 4s; }

                /* 6. Blueprint fades to focus on title */
                @keyframes fade-blueprint { to { opacity: 0.2; } }
                .blueprint { animation: materialize-blueprint 0.5s ease-out forwards 1s, fade-blueprint 1s ease-in-out forwards 4.5s; }

                /* 7. Title appears */
                @keyframes reveal-title {
                    from { opacity: 0; letter-spacing: 10px; }
                    to { opacity: 1; letter-spacing: normal; }
                }
                .title-text { animation: reveal-title 1.5s cubic-bezier(0.19, 1, 0.22, 1) forwards 4.8s; }
            `}</style>
            
            <div className="min-h-screen bg-slate-900 text-white font-sans overflow-hidden bg-grid">
                <div className="mouse-glow"></div>
                <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                    <div className="absolute -top-1/4 -left-1/4 w-1/2 h-1/2 bg-cyan-500/80 rounded-full filter blur-[200px] pulse-glow-1"></div>
                    <div className="absolute -bottom-1/4 -right-1/4 w-1/2 h-1/2 bg-indigo-600/70 rounded-full filter blur-[200px] pulse-glow-2"></div>
                </div>

                <div className="relative z-10">
                    <section className="min-h-screen flex flex-col justify-center items-center text-center px-4">
                        <HolographicBlueprintAnimation />
                        <p className="mt-4 max-w-2xl text-lg md:text-xl text-gray-300 animate-slow-fade-in opacity-0" style={{ animationDelay: '5.8s' }}>
                            Your AI-Powered Cricket Strategist. Instantly Analyze Matchups. Devise Winning Plans.
                        </p>
                        
                        {/* Prominent Get Started Section */}
                        <div className="mt-12 flex flex-col items-center animate-slow-fade-in opacity-0" style={{ animationDelay: '6.1s' }}>
                            <h3 className="text-2xl md:text-3xl font-bold text-white mb-4">
                                Ready to Dominate the Game?
                            </h3>
                            <p className="text-lg text-cyan-300 mb-8 max-w-md">
                                Unlock the power of AI-driven cricket strategy and outsmart your opponents
                            </p>
                            <button 
                                onClick={onGetStarted}
                                className="group px-12 py-6 bg-gradient-to-r from-cyan-500 to-blue-500 text-slate-900 font-bold text-xl rounded-xl shadow-2xl shadow-cyan-500/40 transition-all duration-300 ease-in-out hover:from-cyan-400 hover:to-blue-400 hover:-translate-y-2 hover:shadow-2xl hover:shadow-cyan-400/60 transform hover:scale-105"
                            >
                                <span className="flex items-center">
                                    Get Started Now
                                    <ArrowRight className="ml-3 h-7 w-7 transition-transform duration-300 group-hover:translate-x-2" />
                                </span>
                            </button>
                        </div>
                    </section>

                    <section id="features" className="py-20 sm:py-32 px-4">
                        <div className="max-w-6xl mx-auto">
                            <div className="text-center mb-16">
                                <h2 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">Unleash Your Strategic Edge</h2>
                                <p className="mt-4 text-lg text-gray-400">Everything you need to outsmart the competition.</p>
                            </div>
                            <div className="grid md:grid-cols-3 gap-8">
                                {features.map((feature, index) => <FeatureCard key={index} index={index} {...feature} />)}
                            </div>
                        </div>
                    </section>
                </div>

                <footer className="relative z-10 text-center py-8 border-t border-slate-800">
                    <p className="text-gray-500">&copy; {new Date().getFullYear()} Tactics Master. All Rights Reserved.</p>
                </footer>

                {/* Floating Get Started Button */}
                <div className="fixed bottom-8 right-8 z-50">
                    <button 
                        onClick={onGetStarted}
                        className="group flex items-center px-6 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-bold rounded-full shadow-2xl shadow-cyan-500/40 transition-all duration-300 ease-in-out hover:from-cyan-400 hover:to-blue-400 hover:-translate-y-1 hover:shadow-2xl hover:shadow-cyan-400/60 transform hover:scale-110"
                    >
                        <span className="flex items-center">
                            Start Analysis
                            <ArrowRight className="ml-2 h-5 w-5 transition-transform duration-300 group-hover:translate-x-1" />
                        </span>
                    </button>
                </div>
            </div>
        </>
    );
};

export default WelcomePage;
