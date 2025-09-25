import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Copy, Download, Share2, Target, Users, TrendingUp } from 'lucide-react';
import jsPDF from 'jspdf';

const AnalysisDisplay = ({ analysis }) => {
  // Add custom styles for markdown content
  React.useEffect(() => {
    const style = document.createElement('style');
    style.textContent = `
      .markdown-content h1, .markdown-content h2, .markdown-content h3, 
      .markdown-content h4, .markdown-content h5, .markdown-content h6 {
        color: #ffffff;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
      }
      .markdown-content h1 {
        font-size: 1.5rem;
        color: #06b6d4;
        border-bottom: 2px solid #06b6d4;
        padding-bottom: 0.5rem;
      }
      .markdown-content h2 {
        font-size: 1.25rem;
        color: #06b6d4;
        margin-top: 2rem;
      }
      .markdown-content h3 {
        font-size: 1.1rem;
        color: #06b6d4;
        margin-top: 1.5rem;
      }
      .markdown-content p {
        color: #ffffff;
        margin-bottom: 1rem;
        line-height: 1.7;
        font-size: 1rem;
        font-weight: 400;
      }
      .markdown-content ul, .markdown-content ol {
        color: #ffffff;
        margin-bottom: 1rem;
        padding-left: 1.5rem;
      }
      .markdown-content li {
        margin-bottom: 0.5rem;
        color: #ffffff;
      }
      .markdown-content strong {
        color: #06b6d4;
        font-weight: 600;
      }
      .markdown-content code {
        background-color: rgba(6, 182, 212, 0.1);
        color: #06b6d4;
        padding: 0.2rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.875rem;
      }
      .markdown-content pre {
        background-color: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(6, 182, 212, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        overflow-x: auto;
        margin: 1rem 0;
      }
      .markdown-content blockquote {
        border-left: 4px solid #06b6d4;
        padding-left: 1rem;
        margin: 1rem 0;
        color: #ffffff;
        font-style: italic;
        background-color: rgba(6, 182, 212, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
      }
    `;
    document.head.appendChild(style);
    return () => document.head.removeChild(style);
  }, []);
  const handleCopy = () => {
    navigator.clipboard.writeText(analysis.response);
  };

  const handleDownload = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    let yPosition = 20;
    const lineHeight = 7;
    const margin = 20;
    const maxWidth = pageWidth - (margin * 2);

    // Helper function to add text with word wrapping
    const addText = (text, fontSize = 12, isBold = false, color = [0, 0, 0]) => {
      doc.setFontSize(fontSize);
      doc.setTextColor(color[0], color[1], color[2]);
      if (isBold) {
        doc.setFont(undefined, 'bold');
      } else {
        doc.setFont(undefined, 'normal');
      }
      
      const lines = doc.splitTextToSize(text, maxWidth);
      lines.forEach(line => {
        if (yPosition > pageHeight - 20) {
          doc.addPage();
          yPosition = 20;
        }
        doc.text(line, margin, yPosition);
        yPosition += lineHeight;
      });
    };

    // Helper function to add a line break
    const addLineBreak = (spacing = 1) => {
      yPosition += lineHeight * spacing;
    };

    // Header
    addText('TACTICS MASTER - CRICKET ANALYSIS REPORT', 16, true, [6, 182, 212]);
    addLineBreak(0.5);
    addText(`Generated on: ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}`, 10, false, [100, 100, 100]);
    addLineBreak(1);

    // Analysis Type
    const analysisInfo = getAnalysisType();
    addText(`Analysis Type: ${analysisInfo.type}`, 14, true, [6, 182, 212]);
    addLineBreak(1);

    // Analysis Content
    addText('ANALYSIS RESULTS:', 12, true, [0, 0, 0]);
    addLineBreak(0.5);

    // Clean and format the response text
    const cleanText = analysis.response
      .replace(/\*\*(.*?)\*\*/g, '$1') // Remove markdown bold
      .replace(/\*(.*?)\*/g, '$1') // Remove markdown italic
      .replace(/#{1,6}\s*/g, '') // Remove markdown headers
      .replace(/```[\s\S]*?```/g, (match) => {
        // Convert code blocks to plain text
        return match.replace(/```[\s\S]*?```/g, '').trim();
      })
      .replace(/`(.*?)`/g, '$1') // Remove inline code
      .replace(/\n\s*\n/g, '\n\n') // Clean up multiple newlines
      .trim();

    // Split content into paragraphs and add them
    const paragraphs = cleanText.split('\n\n').filter(p => p.trim().length > 0);
    paragraphs.forEach(paragraph => {
      if (paragraph.trim().length > 0) {
        addText(paragraph.trim(), 11, false, [0, 0, 0]);
        addLineBreak(0.5);
      }
    });

    // Add sources if available
    if (analysis.sources && analysis.sources.length > 0) {
      addLineBreak(1);
      addText('DATA SOURCES:', 12, true, [6, 182, 212]);
      addLineBreak(0.5);
      analysis.sources.forEach(source => {
        addText(`• ${source}`, 10, false, [100, 100, 100]);
        addLineBreak(0.3);
      });
    }

    // Footer
    addLineBreak(2);
    addText('Generated by Tactics Master - AI-Powered Cricket Analysis', 10, false, [100, 100, 100]);
    addText('© 2024 Tactics Master. All rights reserved.', 8, false, [150, 150, 150]);

    // Save the PDF
    const fileName = `cricket-analysis-${analysisInfo.type.toLowerCase().replace(/\s+/g, '-')}-${new Date().toISOString().split('T')[0]}.pdf`;
    doc.save(fileName);
  };

  const getAnalysisType = () => {
    if (analysis.response.includes('Tactical Analysis:')) {
      return { type: 'Player Analysis', icon: Target, color: 'text-cyan-400' };
    } else if (analysis.response.includes('Team Analysis:')) {
      return { type: 'Team Analysis', icon: Users, color: 'text-cyan-400' };
    } else if (analysis.response.includes('Matchup Analysis')) {
      return { type: 'Matchup Analysis', icon: TrendingUp, color: 'text-cyan-400' };
    }
    return { type: 'General Analysis', icon: Target, color: 'text-cyan-400' };
  };

  const analysisInfo = getAnalysisType();
  const IconComponent = analysisInfo.icon;

  return (
    <div className="bg-slate-800/60 backdrop-blur-sm rounded-lg shadow-lg border border-cyan-500/20 p-6 mb-6">
      <div className="mb-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-cyan-500 to-blue-500 rounded-lg">
              <IconComponent className="h-6 w-6 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-semibold text-white">
                {analysisInfo.type}
              </h2>
              <p className="text-sm text-cyan-300">
                Analysis completed successfully
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={handleCopy}
              className="flex items-center px-3 py-2 text-sm text-cyan-300 hover:text-white hover:bg-cyan-500/20 rounded-lg transition-all duration-300"
            >
              <Copy className="h-4 w-4 mr-1" />
              Copy
            </button>
            
            <button
              onClick={handleDownload}
              className="flex items-center px-3 py-2 text-sm text-cyan-300 hover:text-white hover:bg-cyan-500/20 rounded-lg transition-all duration-300"
            >
              <Download className="h-4 w-4 mr-1" />
              Download
            </button>
          </div>
        </div>
      </div>

      <div className="bg-slate-700/30 rounded-lg p-6 border border-cyan-500/10">
        <div className="prose prose-invert max-w-none markdown-content">
          <ReactMarkdown>{analysis.response}</ReactMarkdown>
        </div>
      </div>

      {analysis.sources && analysis.sources.length > 0 && (
        <div className="mt-6 pt-6 border-t border-cyan-500/20">
          <h3 className="text-sm font-medium text-cyan-300 mb-3">Data Sources:</h3>
          <div className="flex flex-wrap gap-2">
            {analysis.sources.map((source, index) => (
              <span
                key={index}
                className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-cyan-500/20 text-cyan-300 border border-cyan-500/30"
              >
                {source}
              </span>
            ))}
          </div>
        </div>
      )}

      {analysis.analysis && Object.keys(analysis.analysis).length > 0 && (
        <div className="mt-6 pt-6 border-t border-cyan-500/20">
          <h3 className="text-sm font-medium text-cyan-300 mb-3">Raw Analysis Data:</h3>
          <pre className="bg-slate-700/50 p-4 rounded-lg overflow-x-auto text-sm text-cyan-200 border border-cyan-500/20">
            {JSON.stringify(analysis.analysis, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default AnalysisDisplay;
