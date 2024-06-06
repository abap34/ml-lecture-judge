import React, { useState, useEffect, useRef } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useParams } from 'react-router-dom';
import { Container, Button, Typography, Box, List, ListItem, ListItemText, Drawer, ListItemButton, AppBar, Toolbar, CssBaseline, IconButton, Divider } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import { useCodeMirror } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeHighlight from 'rehype-highlight';

// カスタムテーマの作成
const theme = createTheme({
  palette: {
    primary: {
      main: '#ff9854', // 薄いオレンジ
    },
    secondary: {
      main: '#FFA726',
    },
  },
  typography: {
    h3: {
      fontFamily: 'Roboto, sans-serif',
      fontWeight: 700,
      color: '#333',
    },
    body1: {
      fontFamily: 'Arial, sans-serif',
      color: '#555',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          textTransform: 'none',
          fontSize: '16px',
          backgroundColor: '#ff9854',
          '&:hover': {
            backgroundColor: '#FFE0B2',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ff9854',
        },
      },
    },
  },
});

function ProblemList({ onClose }) {
  const [problems, setProblems] = useState([]);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await axios.get('http://localhost:8000/problems');
        setProblems(response.data.problems);
      } catch (error) {
        console.error('There was an error fetching the problems!', error);
      }
    };

    fetchProblems();
  }, []);

  return (
    <List>
      {Array.isArray(problems) && problems.map((problem) => (
        <ListItem key={problem.name}>
          <ListItemButton component={Link} to={`/problems/${problem.name}`} onClick={onClose}>
            <ListItemText primary={problem.title} />
          </ListItemButton>
        </ListItem>
      ))}
    </List>
  );
}

function ProblemDetail() {
  const { problemName } = useParams();
  const [problemSummary, setProblemSummary] = useState({});
  const [problemConstraint, setProblemConstraint] = useState({});
  const [problemContent, setProblemContent] = useState('');
  const [code, setCode] = useState('');

  useEffect(() => {
    const fetchProblemContent = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/problems/${problemName}`);
        const data = response.data.problem;
        setProblemSummary(data.summary);
        setProblemConstraint(data.constraint);
        setProblemContent(response.data.description);
      } catch (error) {
        console.error('There was an error fetching the problem content!', error);
      }
    };

    fetchProblemContent();
  }, [problemName]);

  const handleCodeSubmit = async () => {
    try {
      await axios.post('http://localhost:8000/submit', { code });
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
        <Typography variant="body1" sx={{ marginRight: 2 }}>Time Limit: {problemConstraint.time} [ms] </Typography>
        <Typography variant="body1">Memory Limit: {problemConstraint.memory} [MB] </Typography>
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
          Submit Code
        </Button>
      </Box>
    </Container>
  );
}

function Welcome() {
  return (
    <Container maxWidth="md" style={{ marginTop: '50px', backgroundColor: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome!
      </Typography>
      <Typography variant="body1" gutterBottom>
        Please select a problem from the sidebar to get started.
      </Typography>
    </Container>
  );
}

function App() {
  const [isDrawerOpen, setDrawerOpen] = useState(false);

  const toggleDrawer = () => {
    setDrawerOpen(!isDrawerOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <Router>
        <CssBaseline />
        <AppBar position="fixed">
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={toggleDrawer}
              sx={{ mr: 2, ...(isDrawerOpen && { display: 'none' }) }}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" noWrap>
              <Link to="/" style={{ textDecoration: 'none', color: 'white' }}> ml-lecture online judge </Link>
            </Typography>
          </Toolbar>
        </AppBar>
        <Box sx={{ display: 'flex' }}>
          <Drawer
            variant="temporary"
            open={isDrawerOpen}
            onClose={toggleDrawer}
            sx={{
              '& .MuiDrawer-paper': {
                width: 240,
              },
            }}
          >
            <Toolbar>
              <IconButton onClick={toggleDrawer}>
                <CloseIcon />
              </IconButton>
            </Toolbar>
            <ProblemList onClose={toggleDrawer} />
          </Drawer>
          <Box
            component="main"
            sx={{ flexGrow: 1, bgcolor: 'background.default', p: 3 }}
          >
            <Toolbar />
            <Routes>
              <Route path="/problems/:problemName" element={<ProblemDetail />} />
              <Route path="/" element={<Welcome />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
