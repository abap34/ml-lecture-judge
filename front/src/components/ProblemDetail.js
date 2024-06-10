import React, { useState, useEffect, useRef } from 'react';
import { Container, Button, Typography, Box, Divider } from '@mui/material';
import { useParams, useNavigate } from 'react-router-dom';
import { useCodeMirror } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';

function ProblemDetail() {
  const { problemName } = useParams();
  const navigate = useNavigate();
  const [problemSummary, setProblemSummary] = useState({});
  const [problemConstraints, setProblemConstraints] = useState({});
  const [problemContent, setProblemContent] = useState('');
  const [code, setCode] = useState('');

  useEffect(() => {
    const fetchProblemContent = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/problems/${problemName}`);
        const data = response.data.problem;
        setProblemSummary(data.summary);
        setProblemConstraints(data.constraints);
        setProblemContent(response.data.description);
      } catch (error) {
        console.error('There was an error fetching the problem content!', error);
      }
    };

    fetchProblemContent();
  }, [problemName]);

  const handleCodeSubmit = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/submit/${problemName}`, {
        code: code,
        username: 'testuser',
        problem_name: problemName,
      });
      const id = response.data.task_id;
      console.log(`Submitted! Task ID: ${id}`);
      navigate(`/result/${id}`);
    } catch (error) {
      console.error("There was an error submitting the code!", error);
    }
  };

  const editor = useRef(null);
  const { setContainer } = useCodeMirror({
    container: editor.current,
    extensions: [python()],
    value: '',
    options: {
      lineNumbers: true,
      lineWrapping: true,
    },
    onChange: (value, viewUpdate) => {
      setCode(value);
    },
  });

  useEffect(() => {
    if (editor.current) {
      setContainer(editor.current);
    }
  }, [setContainer]);

  return (
    <Container maxWidth="md" style={{ marginTop: '50px', backgroundColor: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        {problemSummary.title}
      </Typography>

      <Box display="flex" justifyContent="flex-start" mb={2}>
        <Typography variant="body1" sx={{ marginRight: 2 }}>Points: {problemSummary.points}</Typography>
        <Typography variant="body1" sx={{ marginRight: 2 }}>Time Limit: {problemConstraints.time} [ms] </Typography>
        <Typography variant="body1">Memory Limit: {problemConstraints.memory} [MB] </Typography>
      </Box>

      <Divider />
      <ReactMarkdown rehypePlugins={[rehypeKatex, rehypeHighlight]} remarkPlugins={[remarkMath]}>
        {problemContent}
      </ReactMarkdown>
      <Box mt={4} width="100%">
        <div
          ref={editor}
          style={{
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '10px',
            height: '400px',
            overflow: 'auto',
            backgroundColor: '#fff'
          }}
        ></div>
        <Button variant="contained" color="primary" onClick={handleCodeSubmit} style={{ marginTop: '20px' }}>
          Submit !
        </Button>
      </Box>
    </Container>
  );
}

export default ProblemDetail;
