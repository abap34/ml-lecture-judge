import React, { useState, useEffect, useRef } from 'react';
import { Container, Button, Typography, Box } from '@mui/material';
import { useCodeMirror } from '@uiw/react-codemirror';
import axios from 'axios';

function App() {
  const [code, setCode] = useState('');
  const [problemTitle, setProblemTitle] = useState('Sample Problem Title');
  const [problemContent, setProblemContent] = useState('Here is the problem description...');

  const handleCodeSubmit = async () => {
    try {
      const response = await axios.post('http://localhost:8000/submit', { code });
      console.log(`Response json: ${JSON.stringify(response.data)}`);
    } catch (error) {
      console.error("There was an error submitting the code!", error);
    }
  };

  const editor = useRef(null);
  const { setContainer } = useCodeMirror({
    container: editor.current,
    value: '',
    options: {
      mode: 'python',
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
    <Container maxWidth="md" style={{ marginTop: '50px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        {problemTitle}
      </Typography>
      <Typography variant="body1" gutterBottom>
        {problemContent}
      </Typography>
      <Box mt={4} width="100%">
        <div
          ref={editor}
          style={{
            border: '1px solid #ddd',
            borderRadius: '4px',
            padding: '10px',
            height: '400px',
            overflow: 'auto'
          }}
        ></div>
        <Button variant="contained" color="primary" onClick={handleCodeSubmit} style={{ marginTop: '20px' }}>
          Submit Code
        </Button>
      </Box>
    </Container>
  );
}

export default App;
