import React, { useState, useEffect } from 'react';
import { 
  Upload, Download, FileText, Target, TrendingUp, AlertCircle, 
  CheckCircle, BookOpen, Calculator, Filter, Save, Eye
} from 'lucide-react';

const AdmissionEvaluator = () => {
  const [transcript, setTranscript] = useState(null);
  const [targetUniversity, setTargetUniversity] = useState('');
  const [programType, setProgramType] = useState('Masters');
  const [evaluation, setEvaluation] = useState(null);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [universities, setUniversities] = useState([]);

  useEffect(() => {
    // Load universities from API
    fetch('http://localhost:8000/rankings')
      .then(res => res.json())
      .then(data => {
        setUniversities(data.slice(0, 50)); // Top 50 universities
      })
      .catch(err => console.log('Error loading universities:', err));
  }, []);

  const handleTranscriptUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        // Parse transcript data (simplified for demo)
        const transcriptData = {
          fileName: file.name,
          content: e.target.result,
          gpa: Math.random() * 2 + 2, // Random GPA 2.0-4.0
          courses: generateMockCourses(),
          testScores: {
            gre: Math.floor(Math.random() * 40 + 150), // 150-190
            toefl: Math.floor(Math.random() * 20 + 90), // 90-110
            gmat: Math.floor(Math.random() * 100 + 600) // 600-700
          }
        };
        setTranscript(transcriptData);
      };
      reader.readAsText(file);
    }
  };

  const generateMockCourses = () => {
    const subjects = ['Mathematics', 'Physics', 'Computer Science', 'Chemistry', 'Biology', 'Engineering'];
    return subjects.map(subject => ({
      name: subject,
      grade: ['A', 'A-', 'B+', 'B', 'B-'][Math.floor(Math.random() * 5)],
      credits: Math.floor(Math.random() * 3 + 2)
    }));
  };

  const evaluateTranscript = async () => {
    if (!transcript || !targetUniversity) return;

    setIsEvaluating(true);
    
    try {
      const response = await fetch('http://localhost:8000/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          target_university: targetUniversity,
          gpa: transcript.gpa,
          test_scores: transcript.testScores,
          program_type: programType
        })
      });

      if (response.ok) {
        const evaluationResult = await response.json();
        setEvaluation(evaluationResult);
      } else {
        console.error('Evaluation failed');
        // Fallback to client-side calculation
        const targetData = universities.find(u => u.university_name === targetUniversity);
        const targetRank = targetData ? targetData.qs_rank : 50;
        
        const acceptanceProbability = Math.min(95, Math.max(5, 
          (transcript.gpa / 4.0) * 30 + 
          ((transcript.testScores.gre - 150) / 40) * 20 + 
          Math.max(0, (100 - targetRank) / 100) * 20 + 
          Math.random() * 30
        ));

        const evaluationResult = {
          academics: acceptanceProbability > 70 ? 'A' : acceptanceProbability > 50 ? 'B' : 'C',
          gpaConverted: transcript.gpa,
          courseworkStatus: acceptanceProbability > 60 ? 'Passed' : 'Needs Improvement',
          gaps: identifyGaps(transcript, targetData),
          acceptanceProbability: Math.round(acceptanceProbability),
          recommendations: generateRecommendations(acceptanceProbability, transcript),
          targetProfile: targetData
        };

        setEvaluation(evaluationResult);
      }
    } catch (error) {
      console.error('Error during evaluation:', error);
      // Fallback calculation
      const acceptanceProbability = Math.min(95, Math.max(5, 
        (transcript.gpa / 4.0) * 40 + Math.random() * 60
      ));
      
      setEvaluation({
        academics: acceptanceProbability > 70 ? 'A' : 'B',
        gpaConverted: transcript.gpa,
        courseworkStatus: 'Passed',
        gaps: ['Consider improving test scores'],
        acceptanceProbability: Math.round(acceptanceProbability),
        recommendations: ['Strengthen application materials'],
        targetProfile: universities.find(u => u.university_name === targetUniversity)
      });
    } finally {
      setIsEvaluating(false);
    }
  };

  const calculateCourseScore = (courses) => {
    const gradePoints = { 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7 };
    const totalPoints = courses.reduce((sum, course) => 
      sum + (gradePoints[course.grade] || 0) * course.credits, 0);
    const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
    return (totalPoints / totalCredits) / 4.0;
  };

  const identifyGaps = (transcript, targetData) => {
    const gaps = [];
    if (transcript.gpa < 3.5) gaps.push('GPA below competitive threshold');
    if (transcript.testScores.gre < 160) gaps.push('GRE score could be improved');
    if (transcript.testScores.toefl < 100) gaps.push('TOEFL score below recommended level');
    return gaps;
  };

  const generateRecommendations = (probability, transcript) => {
    const recommendations = [];
    if (probability < 70) {
      recommendations.push('Strengthen Statement of Purpose');
      recommendations.push('Gain relevant research experience');
    }
    if (transcript.gpa < 3.7) {
      recommendations.push('Consider retaking courses to improve GPA');
    }
    if (transcript.testScores.gre < 165) {
      recommendations.push('Retake GRE to improve quantitative score');
    }
    return recommendations;
  };

  const exportReport = () => {
    if (!evaluation) return;
    
    const reportContent = `
ADMISSION EVALUATION REPORT
==========================

Applicant: John Doe
Target University: ${targetUniversity}
Program Type: ${programType}

EVALUATION RESULTS
------------------
Academics: ${evaluation.academics}
GPA (Converted): ${evaluation.gpaConverted}/4.0
Coursework Status: ${evaluation.courseworkStatus}
Acceptance Probability: ${evaluation.acceptanceProbability}%

Identified Gaps:
${evaluation.gaps.map(gap => `- ${gap}`).join('\n')}

Recommendations:
${evaluation.recommendations.map(rec => `- ${rec}`).join('\n')}

Generated on: ${new Date().toLocaleDateString()}
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `admission_report_${targetUniversity.replace(/\s+/g, '_')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="admission-evaluator" style={{ display: 'flex', gap: '2rem', height: '100vh' }}>
      {/* Left Side - QS Analysis Board */}
      <div style={{ flex: 1, borderRight: '1px solid #ddd', paddingRight: '2rem', overflowY: 'auto' }}>
        <h2 style={{ marginBottom: '1.5rem', color: 'var(--primary)' }}>QS Analysis Board</h2>
        
        {targetUniversity && evaluation?.targetProfile && (
          <div className="target-profile" style={{ 
            background: 'linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%)',
            color: 'white', 
            padding: '1.5rem', 
            borderRadius: '12px', 
            marginBottom: '2rem' 
          }}>
            <h3>{targetUniversity}</h3>
            <p>Rank: #{evaluation.targetProfile.qs_rank}</p>
            <p>Region: {evaluation.targetProfile.region}</p>
            <p>Type: {evaluation.targetProfile.university_type}</p>
          </div>
        )}

        <div className="comparison-metrics" style={{ marginBottom: '2rem' }}>
          <h4>Comparison Metrics</h4>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '1rem' }}>
            <div className="metric-card" style={{ 
              background: '#f8f9fa', 
              padding: '1rem', 
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <Calculator size={24} style={{ color: 'var(--primary)' }} />
              <p>Avg GPA: 3.8</p>
            </div>
            <div className="metric-card" style={{ 
              background: '#f8f9fa', 
              padding: '1rem', 
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <TrendingUp size={24} style={{ color: 'var(--primary)' }} />
              <p>Avg GRE: 165</p>
            </div>
            <div className="metric-card" style={{ 
              background: '#f8f9fa', 
              padding: '1rem', 
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <BookOpen size={24} style={{ color: 'var(--primary)' }} />
              <p>Employability: 95%</p>
            </div>
            <div className="metric-card" style={{ 
              background: '#f8f9fa', 
              padding: '1rem', 
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              <Target size={24} style={{ color: 'var(--primary)' }} />
              <p>Research Output: 92%</p>
            </div>
          </div>
        </div>

        <div className="peer-comparison">
          <h4>Top 10 Peer Institutions</h4>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {universities.slice(0, 10).map((uni, index) => (
              <div key={uni.university_id} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                padding: '0.5rem 0',
                borderBottom: '1px solid #eee'
              }}>
                <span>#{index + 1} {uni.university_name}</span>
                <span style={{ color: 'var(--primary)', fontWeight: 'bold' }}>
                  {uni.qs_rank ? `Rank ${uni.qs_rank}` : 'N/A'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Right Side - Consulting Report */}
      <div style={{ flex: 1, paddingLeft: '2rem', overflowY: 'auto' }}>
        <h2 style={{ marginBottom: '1.5rem', color: 'var(--primary)' }}>Admission Assessment</h2>
        
        {/* Control Panel */}
        <div className="control-panel" style={{ 
          background: '#f8f9fa', 
          padding: '1rem', 
          borderRadius: '8px', 
          marginBottom: '2rem',
          display: 'flex',
          gap: '1rem',
          alignItems: 'center',
          flexWrap: 'wrap'
        }}>
          <label className="upload-btn" style={{ 
            background: 'var(--primary)', 
            color: 'white', 
            padding: '0.5rem 1rem', 
            borderRadius: '6px',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}>
            <Upload size={16} />
            Import Transcript
            <input type="file" onChange={handleTranscriptUpload} style={{ display: 'none' }} />
          </label>
          
          <select 
            value={targetUniversity} 
            onChange={(e) => setTargetUniversity(e.target.value)}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="">Select Target University</option>
            {universities.map(uni => (
              <option key={uni.university_id} value={uni.university_name}>
                {uni.university_name}
              </option>
            ))}
          </select>
          
          <select 
            value={programType} 
            onChange={(e) => setProgramType(e.target.value)}
            style={{ padding: '0.5rem', borderRadius: '6px', border: '1px solid #ddd' }}
          >
            <option value="Masters">Masters</option>
            <option value="PhD">PhD</option>
            <option value="Undergraduate">Undergraduate</option>
          </select>
          
          <button 
            onClick={evaluateTranscript}
            disabled={!transcript || !targetUniversity || isEvaluating}
            style={{ 
              background: isEvaluating ? '#ccc' : 'var(--secondary)', 
              color: 'white', 
              padding: '0.5rem 1rem', 
              borderRadius: '6px',
              cursor: isEvaluating ? 'not-allowed' : 'pointer'
            }}
          >
            {isEvaluating ? 'Evaluating...' : 'Evaluate'}
          </button>
          
          <button 
            onClick={exportReport}
            disabled={!evaluation}
            style={{ 
              background: evaluation ? 'var(--success)' : '#ccc', 
              color: 'white', 
              padding: '0.5rem 1rem', 
              borderRadius: '6px',
              cursor: evaluation ? 'pointer' : 'not-allowed',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}
          >
            <Download size={16} />
            Export Report
          </button>
        </div>

        {/* User Info */}
        <div className="user-info" style={{ 
          background: '#e8f4f8', 
          padding: '1rem', 
          borderRadius: '8px', 
          marginBottom: '2rem' 
        }}>
          <p><strong>USER NAME:</strong> John Doe</p>
          <p><strong>TARGET:</strong> {targetUniversity || 'Not Selected'}</p>
        </div>

        {/* Evaluation Report */}
        {evaluation && (
          <div className="evaluation-report">
            <h3>EVALUATION REPORT</h3>
            <div style={{ 
              background: '#f8f9fa', 
              padding: '1.5rem', 
              borderRadius: '8px', 
              marginBottom: '2rem' 
            }}>
              <div className="report-item" style={{ marginBottom: '1rem' }}>
                <strong>1. Academics:</strong> 
                <span style={{ 
                  color: evaluation.academics === 'A' ? 'green' : 
                         evaluation.academics === 'B' ? 'orange' : 'red',
                  marginLeft: '0.5rem'
                }}>
                  {evaluation.academics} (Matches &gt;{evaluation.acceptanceProbability}% criteria)
                </span>
              </div>
              
              <div className="report-item" style={{ marginBottom: '1rem' }}>
                <strong>2. GPA/Scale Conversion:</strong> {evaluation.gpaConverted}/4.0 (Estimated)
              </div>
              
              <div className="report-item" style={{ marginBottom: '1rem' }}>
                <strong>3. Relevant Coursework Check:</strong> 
                <span style={{ color: evaluation.courseworkStatus === 'Passed' ? 'green' : 'orange' }}>
                  {evaluation.courseworkStatus}
                </span>
              </div>
              
              <div className="report-item" style={{ marginBottom: '1rem' }}>
                <strong>4. Gaps Identified:</strong> 
                <span style={{ color: 'red' }}>
                  {evaluation.gaps.length > 0 ? evaluation.gaps.join(', ') : 'None identified'}
                </span>
              </div>
            </div>

            {/* Acceptance Probability */}
            <div className="acceptance-probability" style={{ 
              background: evaluation.acceptanceProbability > 70 ? '#d4edda' : 
                         evaluation.acceptanceProbability > 50 ? '#fff3cd' : '#f8d7da',
              padding: '1.5rem', 
              borderRadius: '8px', 
              textAlign: 'center',
              marginBottom: '2rem',
              border: `2px solid ${
                evaluation.acceptanceProbability > 70 ? '#28a745' : 
                evaluation.acceptanceProbability > 50 ? '#ffc107' : '#dc3545'
              }`
            }}>
              <h3>ACCEPTANCE PROBABILITY</h3>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', margin: '1rem 0' }}>
                {evaluation.acceptanceProbability}% - {
                  evaluation.acceptanceProbability > 70 ? 'High' : 
                  evaluation.acceptanceProbability > 50 ? 'Medium' : 'Low'
                }
              </div>
            </div>

            {/* Recommendations */}
            <div className="recommendations" style={{ 
              background: '#e8f4f8', 
              padding: '1.5rem', 
              borderRadius: '8px' 
            }}>
              <h3>RECOMMENDATIONS:</h3>
              <ul style={{ paddingLeft: '1.5rem' }}>
                {evaluation.recommendations.map((rec, index) => (
                  <li key={index} style={{ marginBottom: '0.5rem' }}>{rec}</li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdmissionEvaluator;
