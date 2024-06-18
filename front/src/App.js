import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useNavigate } from 'react-router-dom';
import { Typography, Box, Drawer, AppBar, Toolbar, CssBaseline, IconButton, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Button } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuIcon from '@mui/icons-material/Menu';
import CloseIcon from '@mui/icons-material/Close';
import ProblemList from './components/ProblemList';
import ProblemDetail from './components/ProblemDetail';
import Welcome from './components/Welcome';
import SubmissionResult from './components/SubmissionResult';
import axios from 'axios';

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
          backgroundColor: '#FFFFFF', 
          color: '#ff9854', 
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


const AppContent = () => {
  const [isDrawerOpen, setDrawerOpen] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/login_status', { withCredentials: true });
        if (response.data.logged_in) {
          console.log('User is logged in');
          setIsLoggedIn(true);
          getUserInfo();
        } else {
          console.log('User is not logged in');
          setOpenDialog(true);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, []);

  const getUserInfo = async () => {
    try {
      // get bearer token. get from cookie
      const token = document.cookie.split('=')[1];
      console.log('token:', token);
      
      const response = await axios.get('http://localhost:8000/userinfo', { withCredentials: true });
      console.log('Logged in user:', response.data.userinfo.name);
    } catch (error) {
      console.error('Error getting user info:', error);
    }
  };

  const handleLogin = async () => {
    try {
      window.location.href = 'http://localhost:8000/login';
    } catch (error) {
      console.error('Error during login:', error);
    }
  };

  const toggleDrawer = () => {
    setDrawerOpen(!isDrawerOpen);
  };

  return (
    <>
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
            <Link to="/" style={{ textDecoration: 'none', color: 'white' }}>ml-lecture online judge</Link>
          </Typography>
          <Typography variant="h6" noWrap sx={{ flexGrow: 1 }} />
           Logged in as: {isLoggedIn ? 'testuser' : 'Guest'}
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
      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">{"ログインが必要です"}</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            問題の閲覧・提出はログインが必要です。ログインしますか？
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}  autoFocus>
            キャンセル
          </Button>
          <Button onClick={handleLogin}  autoFocus>
            ログイン
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;
