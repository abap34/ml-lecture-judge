import { Avatar, AvatarGroup, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

const Leaderboard = () => {
  const [userScores, setUserScores] = useState([]);
  const [teamScores, setTeamScores] = useState([]);

  useEffect(() => {
    const fetchUserScores = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/leaderboard/users`, { withCredentials: true });
        setUserScores(response.data);
      } catch (error) {
        console.error('Error fetching user scores:', error);
      }
    };

    const fetchTeamScores = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/leaderboard/teams`, { withCredentials: true });
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

<Typography variant="h4" gutterBottom style={{ marginTop: '20px' }}>
        Team Leaderboard
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell>Team Name</TableCell>
              <TableCell></TableCell>
              <TableCell>Total Points</TableCell>
              <TableCell>Total AC</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {teamScores.map((team, index) => (
              <TableRow key={team.id}>
                <TableCell>{team.rank}</TableCell>
                <TableCell>{team.name}</TableCell>
                <TableCell>
                  <AvatarGroup max={4}>
                    {team.icon_urls.map((url, idx) => (
                      <Avatar key={idx} src={url} />
                    ))}
                  </AvatarGroup>
                </TableCell>
                <TableCell>{team.total_points}</TableCell>
                <TableCell>{team.total_submissions}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>


      <Typography variant="h4" gutterBottom>
        User Leaderboard
      </Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Rank</TableCell>
              <TableCell></TableCell>
              <TableCell>Username</TableCell>
              <TableCell>Total Points</TableCell>
              <TableCell>Total AC</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {userScores.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.rank}</TableCell>
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
    </Container>
  );
};

export default Leaderboard;
