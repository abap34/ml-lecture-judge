import CloseIcon from '@mui/icons-material/Close';
import MenuIcon from '@mui/icons-material/Menu';
import { AppBar, Box, Button, CssBaseline, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Drawer, IconButton, Toolbar, Typography } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link, Route, BrowserRouter as Router, Routes, useLocation } from 'react-router-dom';
import AuthRedirect from './components/Auth';
import Leaderboard from './components/LeaderBoard';
import ProblemDetail from './components/ProblemDetail';
import ProblemList from './components/ProblemList';
import SubmissionResult from './components/SubmissionResult';
import Welcome from './components/Welcome';

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
  const [userName, setUserName] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const checkLoginStatus = async () => {
      try {
        // auth でログイン求めると無限ループする
        if (location.pathname === '/auth') return;

        const response = await axios.get(`${process.env.API_URL}/login_status`, { withCredentials: true });
        if (response.data.logged_in) {
          setIsLoggedIn(true);
          getUserInfo();
        } else {
          setOpenDialog(true);
        }
      } catch (error) {
        console.error('Error checking login status:', error);
      }
    };

    checkLoginStatus();
  }, [location.pathname]);

  const getUserInfo = async () => {
    try {
      const response = await axios.get(`${process.env.API_URL}/traq_name`, { withCredentials: true });
      setUserName(response.data.name);
    } catch (error) {
      console.error('Error getting user info:', error);
    }
  };

  const handleLogin = async () => {
    try {
      window.location.href = `${process.env.API_URL}/login`;
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
          <Box sx={{ flexGrow: 1 }} />
          {isLoggedIn ? (
            <>
              <Typography variant="h6" noWrap sx={{ mr: 2 }}>
                Logged in as: {userName}
              </Typography>
            </>
          ) : (
            <Button color="inherit" onClick={handleLogin} sx={{ ml: 2 }}>
              Login
            </Button>
          )}
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
            <Route path="/leaderboard" element={<Leaderboard />} />
            <Route path="/auth" element={<AuthRedirect />} />
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
          <Button onClick={() => setOpenDialog(false)} autoFocus>
            キャンセル
          </Button>
          <Button onClick={handleLogin} autoFocus>
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
