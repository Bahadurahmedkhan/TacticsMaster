import React from 'react';
import { Brain, Target, Zap, TrendingUp, Users, BarChart3, Cpu, Shield } from 'lucide-react';

const About = ({ onBackToAnalysis }) => {
  const stats = [
    { icon: <Brain className="h-8 w-8 text-cyan-400" />, label: "AI Models", value: "Advanced", description: "Machine Learning" },
    { icon: <Target className="h-8 w-8 text-cyan-400" />, label: "Accuracy", value: "95%+", description: "Prediction Rate" },
    { icon: <Zap className="h-8 w-8 text-cyan-400" />, label: "Speed", value: "< 2s", description: "Analysis Time" },
    { icon: <TrendingUp className="h-8 w-8 text-cyan-400" />, label: "Success", value: "85%", description: "Win Rate" }
  ];

  const features = [
    {
      icon: <Brain className="h-12 w-12 text-cyan-400" />,
      title: "AI-Powered Analysis",
      description: "Advanced machine learning algorithms analyze player performance, match conditions, and historical data to provide strategic insights.",
      color: "from-cyan-500 to-blue-500"
    },
    {
      icon: <BarChart3 className="h-12 w-12 text-cyan-400" />,
      title: "Data-Driven Decisions",
      description: "Real-time statistics and performance metrics help coaches and players make informed tactical decisions during matches.",
      color: "from-blue-500 to-indigo-500"
    },
    {
      icon: <Users className="h-12 w-12 text-cyan-400" />,
      title: "Player Matchups",
      description: "Comprehensive head-to-head analysis between batsmen and bowlers to identify strengths, weaknesses, and optimal strategies.",
      color: "from-indigo-500 to-purple-500"
    },
    {
      icon: <Cpu className="h-12 w-12 text-cyan-400" />,
      title: "Real-Time Processing",
      description: "Instant analysis and recommendations during live matches, adapting to changing conditions and match situations.",
      color: "from-purple-500 to-pink-500"
    }
  ];

  const AnimatedCounter = ({ end, duration = 2000 }) => {
    const [count, setCount] = React.useState(0);
    const [ref, inView] = React.useState(false);

    React.useEffect(() => {
      if (inView) {
        let startTime;
        const animate = (currentTime) => {
          if (!startTime) {
            startTime = currentTime;
          }
          const progress = Math.min((currentTime - startTime) / duration, 1);
          setCount(Math.floor(progress * end));
          if (progress < 1) {
            requestAnimationFrame(animate);
          }
        };
        requestAnimationFrame(animate);
      }
    }, [inView, end, duration]);

    return (
      <div ref={ref} className="text-4xl font-bold text-cyan-400">
        {count}{end === 95 ? '%' : end === 85 ? '%' : end === 2 ? 's' : '+'}
      </div>
    );
  };

  const FloatingIcon = ({ icon, delay = 0 }) => {
    return (
      <div 
        className="absolute opacity-20 text-cyan-400 animate-float"
        style={{ 
          animationDelay: `${delay}s`,
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`
        }}
      >
        {icon}
      </div>
    );
  };

  return (
    <>
      <style>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) rotate(0deg); }
          50% { transform: translateY(-20px) rotate(5deg); }
        }
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 20px rgba(6, 182, 212, 0.3); }
          50% { box-shadow: 0 0 40px rgba(6, 182, 212, 0.6); }
        }
        @keyframes slide-in-left {
          from { transform: translateX(-100px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slide-in-right {
          from { transform: translateX(100px); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
        @keyframes fade-in-up {
          from { transform: translateY(30px); opacity: 0; }
          to { transform: translateY(0); opacity: 1; }
        }
        .animate-float { animation: float 6s ease-in-out infinite; }
        .animate-pulse-glow { animation: pulse-glow 3s ease-in-out infinite; }
        .animate-slide-in-left { animation: slide-in-left 0.8s ease-out; }
        .animate-slide-in-right { animation: slide-in-right 0.8s ease-out; }
        .animate-fade-in-up { animation: fade-in-up 0.8s ease-out; }
      `}</style>
      
      <section id="about" className="py-20 px-4 relative overflow-hidden">
        {/* Background Effects */}
        <div className="absolute inset-0 overflow-hidden">
          <FloatingIcon icon={<Brain className="h-16 w-16" />} delay={0} />
          <FloatingIcon icon={<Target className="h-12 w-12" />} delay={2} />
          <FloatingIcon icon={<Zap className="h-14 w-14" />} delay={4} />
          <FloatingIcon icon={<BarChart3 className="h-10 w-10" />} delay={1} />
          <FloatingIcon icon={<Users className="h-18 w-18" />} delay={3} />
        </div>

        <div className="max-w-7xl mx-auto relative z-10">
          {/* Header */}
          <div className="text-center mb-16 animate-fade-in-up">
            <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-cyan-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent mb-6">
              About Tactics Master
            </h2>
            <p className="text-xl text-cyan-300 max-w-3xl mx-auto leading-relaxed">
              Revolutionizing cricket strategy through cutting-edge AI technology, 
              real-time data analysis, and intelligent tactical recommendations.
            </p>
          </div>

          {/* Stats Section */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-20">
            {stats.map((stat, index) => (
              <div 
                key={index}
                className="text-center p-6 bg-slate-800/40 backdrop-blur-sm rounded-xl border border-cyan-500/20 animate-fade-in-up"
                style={{ animationDelay: `${index * 0.2}s` }}
              >
                <div className="mb-4 flex justify-center">{stat.icon}</div>
                <div className="text-3xl font-bold text-cyan-400 mb-2">{stat.value}</div>
                <div className="text-lg font-semibold text-white mb-1">{stat.label}</div>
                <div className="text-sm text-cyan-300">{stat.description}</div>
              </div>
            ))}
          </div>

          {/* Main Content */}
          <div className="grid lg:grid-cols-2 gap-16 items-center mb-20">
            {/* Left Side - Text Content */}
            <div className="animate-slide-in-left">
              <h3 className="text-4xl font-bold text-white mb-6">
                The Future of Cricket Strategy
              </h3>
              <p className="text-lg text-cyan-300 mb-6 leading-relaxed">
                Tactics Master leverages advanced artificial intelligence to analyze 
                cricket matches in real-time, providing coaches, players, and analysts 
                with unprecedented insights into game dynamics.
              </p>
              <p className="text-lg text-cyan-300 mb-8 leading-relaxed">
                Our platform combines machine learning algorithms with comprehensive 
                cricket databases to deliver strategic recommendations that can change 
                the outcome of matches.
              </p>
              
              <div className="flex flex-wrap gap-4">
                <div className="flex items-center px-4 py-2 bg-cyan-500/20 rounded-full border border-cyan-500/30">
                  <Shield className="h-5 w-5 text-cyan-400 mr-2" />
                  <span className="text-cyan-300">Secure & Reliable</span>
                </div>
                <div className="flex items-center px-4 py-2 bg-cyan-500/20 rounded-full border border-cyan-500/30">
                  <Cpu className="h-5 w-5 text-cyan-400 mr-2" />
                  <span className="text-cyan-300">AI-Powered</span>
                </div>
                <div className="flex items-center px-4 py-2 bg-cyan-500/20 rounded-full border border-cyan-500/30">
                  <Zap className="h-5 w-5 text-cyan-400 mr-2" />
                  <span className="text-cyan-300">Real-Time</span>
                </div>
              </div>
            </div>

            {/* Right Side - Animated Visualization */}
            <div className="animate-slide-in-right">
              <div className="relative">
                <div className="w-full h-96 bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl border border-cyan-500/20 p-8 animate-pulse-glow">
                  <div className="text-center mb-6">
                    <h4 className="text-2xl font-bold text-cyan-400 mb-2">AI Analysis Engine</h4>
                    <p className="text-cyan-300">Processing match data in real-time</p>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                      <span className="text-cyan-300">Player Performance</span>
                      <div className="w-24 h-2 bg-slate-600 rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full animate-pulse" style={{ width: '85%' }}></div>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                      <span className="text-cyan-300">Match Conditions</span>
                      <div className="w-24 h-2 bg-slate-600 rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full animate-pulse" style={{ width: '92%' }}></div>
                      </div>
                    </div>
                    
                    <div className="flex items-center justify-between p-3 bg-slate-700/50 rounded-lg">
                      <span className="text-cyan-300">Tactical Recommendations</span>
                      <div className="w-24 h-2 bg-slate-600 rounded-full overflow-hidden">
                        <div className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full animate-pulse" style={{ width: '78%' }}></div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-6 text-center">
                    <div className="inline-flex items-center px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full">
                      <div className="w-2 h-2 bg-white rounded-full animate-pulse mr-2"></div>
                      <span className="text-white font-semibold">Analysis Complete</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Features Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div 
                key={index}
                className="group p-6 bg-slate-800/40 backdrop-blur-sm rounded-xl border border-cyan-500/20 hover:border-cyan-500/40 transition-all duration-300 hover:-translate-y-2 animate-fade-in-up"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="mb-4 group-hover:scale-110 transition-transform duration-300">
                  {feature.icon}
                </div>
                <h4 className="text-xl font-bold text-white mb-3">{feature.title}</h4>
                <p className="text-cyan-300 leading-relaxed">{feature.description}</p>
              </div>
            ))}
          </div>

          {/* Call to Action */}
          <div className="text-center mt-20 animate-fade-in-up">
            <h3 className="text-3xl font-bold text-white mb-4">
              Ready to Transform Your Cricket Strategy?
            </h3>
            <p className="text-xl text-cyan-300 mb-8 max-w-2xl mx-auto">
              Join the revolution in cricket analytics and gain the competitive edge 
              with AI-powered tactical insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={onBackToAnalysis}
                className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-500 text-white font-bold text-lg rounded-xl hover:from-cyan-400 hover:to-blue-400 transition-all duration-300 shadow-lg shadow-cyan-500/30 hover:shadow-xl hover:shadow-cyan-400/50 transform hover:scale-105"
              >
                Start Your Analysis
              </button>
              <button 
                onClick={onBackToAnalysis}
                className="px-8 py-4 bg-slate-600 text-white font-bold text-lg rounded-xl hover:bg-slate-500 transition-all duration-300"
              >
                Back to Portal
              </button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default About;
