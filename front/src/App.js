import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { Typography, Box, Drawer, AppBar, Toolbar, CssBaseline, IconButton } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import ProblemList from './components/ProblemList';
import ProblemDetail from './components/ProblemDetail';
import Welcome from './components/Welcome';
import SubmissionResult from './components/SubmissionResult';

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
              <Route path="/result/:taskId" element={<SubmissionResult />} />
              <Route path="/" element={<Welcome />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
