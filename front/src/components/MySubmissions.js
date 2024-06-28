import { Box, Container, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Chip, Link } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';

const MySubmissions = () => {
  const [submissions, setSubmissions] = useState([]);

  useEffect(() => {
    const fetchSubmissions = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/mysubmissions`, { withCredentials: true });
        setSubmissions(response.data);
      } catch (error) {
        console.error('There was an error fetching the submissions!', error);
      }
    };

    fetchSubmissions();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'AC':
        return 'success';
      case 'IE':
        return 'error';
      default:
        return 'warning';
    }
  };

  return (
    <Container maxWidth="md" style={{ marginTop: '50px', padding: '20px', borderRadius: '8px' }}>
      <Typography variant="h3" component="h1" gutterBottom>
        My Submissions
      </Typography>
      
      <Typography variant="body1" gutterBottom>
        (既知の問題: 昔の一部の投稿およびジャッジが正常に動作しなかった投稿は詳細を見てもジャッジ中の状態になっているかもしれません。)
      </Typography>

      <Box p={2} component={Paper}>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell><strong>Problem Name</strong></TableCell>
                <TableCell><strong>Status</strong></TableCell>
                <TableCell><strong>Execution Time</strong></TableCell>
                <TableCell><strong>Submitted At</strong></TableCell>
                <TableCell><strong>Points</strong></TableCell>
                <TableCell><strong>Details</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {submissions.map((submission) => (
                <TableRow key={submission.id}>
                  <TableCell>{submission.problem_name}</TableCell>
                  <TableCell>
                    <Chip label={submission.status} color={getStatusColor(submission.status)} />
                  </TableCell>
                  <TableCell>{submission.execution_time} seconds</TableCell>
                  <TableCell>{new Date(submission.submitted_at).toLocaleString()}</TableCell>
                  <TableCell>{submission.get_points}</TableCell>
                  <TableCell>
                    <Link href={`/result/${submission.id}`} style={{ textDecoration: 'none', color: '#ff9854' }}>
                      View Details
                    </Link>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Container>
  );
};

export default MySubmissions;
