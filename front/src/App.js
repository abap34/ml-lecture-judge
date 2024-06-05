import React, { useState, useEffect, useRef } from 'react';
import { Container, Button, Typography, Box } from '@mui/material';
import { useCodeMirror } from '@uiw/react-codemirror';
import axios from 'axios';

function App() {
  const [code, setCode] = useState('');

  const handleCodeSubmit = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/submit`, { code });
      console.log(`Code length: ${response.data.length}`); // コードの長さを表示
    } catch (error) {
      console.error("There was an error submitting the code!", error);
    }
  };

  // CodeMirrorの設定
  const editor = useRef(null);
  const { setContainer } = useCodeMirror({
    container: editor.current,
    value: '\n\n\n\n\n\n\n\n\n\n\n\n\n\n',
    options: {
      mode: 'python',
      lineNumbers: true,
      lineWrapping: true, // 行の自動折り返し
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
        Code Editor
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
