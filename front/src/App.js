import React, { useState } from 'react';
import { Container, TextField, Button, Typography, Box } from '@mui/material';
import axios from 'axios';

function App() {
  const [username, setUsername] = useState('');
  const [greeting, setGreeting] = useState('');

  const handleInputChange = (e) => {
    setUsername(e.target.value);
  };

  const handleButtonClick = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/${username}`);
      setGreeting(response.data.Hello);
    } catch (error) {
      console.error("There was an error fetching the greeting!", error);
    }
  };

  return (
    <Container maxWidth="sm" style={{ marginTop: '100px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        Welcome
      </Typography>
      <Box display="flex" flexDirection="column" alignItems="center">
        <TextField
          label="Enter your username"
          variant="outlined"
          value={username}
          onChange={handleInputChange}
          style={{ marginBottom: '20px', width: '100%' }}
        />
        <Button variant="contained" color="primary" onClick={handleButtonClick}>
          Submit
        </Button>
        {greeting && (
          <Typography variant="h5" component="h2" style={{ marginTop: '20px' }}>
            Hello, {greeting}!
          </Typography>
        )}
      </Box>
    </Container>
  );
}

export default App;
