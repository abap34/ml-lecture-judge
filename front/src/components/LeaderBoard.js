import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Avatar } from '@mui/material';

const Leaderboard = () => {
  const [userScores, setUserScores] = useState([]);
  const [teamScores, setTeamScores] = useState([]);

  useEffect(() => {
    const fetchUserScores = async () => {
      try {
        const response = await axios.get('http://localhost:8000/leaderboard/users', { withCredentials: true });
        setUserScores(response.data);
      } catch (error) {
        console.error('Error fetching user scores:', error);
      }
    };

    const fetchTeamScores = async () => {
      try {
        const response = await axios.get('http://localhost:8000/leaderboard/teams', { withCredentials: true });
        setTeamScores(response.data);
      } catch (error) {
        console.error('Error fetching team scores:', error);
      }
    };

    fetchUserScores();
    fetchTeamScores();
  }, []);

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        User Leaderboard
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell>Icon</TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Total Points</TableCell>
              <TableCell>Total Submissions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {userScores.map((user, index) => (
              <TableRow key={user.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>
                  <Avatar src={user.icon_url} />
                </TableCell>
                <TableCell>{user.id}</TableCell>
                <TableCell>{user.total_points}</TableCell>
                <TableCell>{user.total_submissions}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Typography variant="h4" gutterBottom style={{ marginTop: '20px' }}>
        Team Leaderboard
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell>Team Name</TableCell>
              <TableCell>Total Points</TableCell>
              <TableCell>Total Submissions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teamScores.map((team, index) => (
              <TableRow key={team.id}>
                <TableCell>{index + 1}</TableCell>
                <TableCell>{team.name}</TableCell>
                <TableCell>{team.total_points}</TableCell>
                <TableCell>{team.total_submissions}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default Leaderboard;
