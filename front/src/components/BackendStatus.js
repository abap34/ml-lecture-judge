import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import axios from 'axios';

const BackendStatus = () => {
  const [status, setStatus] = useState('Checking...');

  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        await axios.get(`${process.env.REACT_APP_API_URL}/`);
        setStatus('Judge server status: OK');
      } catch (error) {
        setStatus('Judge server status: Stopping');
      }
    };

    checkBackendStatus();
    const interval = setInterval(checkBackendStatus, 60000); // 1分ごとに再チェック
    return () => clearInterval(interval);
  }, []);

  return (
    <Box sx={{ position: 'fixed', bottom: 16, right: 16, p: 2, bgcolor: 'background.paper', boxShadow: 3, borderRadius: 2 }}>
      <Typography variant="body2">{status}</Typography>
    </Box>
  );
};

export default BackendStatus;
