import { TableContainer, Table, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function ProblemList({ onClose }) {
  const [problems, setProblms] = useState([]);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/problems`, { withCredentials: true });
        setProblems(response.data);
      } catch (error) {
        console.error('There was an error fetching the problems!', error);
      }
    };

    fetchProblems();
  }, []);

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Title</TableCell>
            <TableCell>Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {Array.isArray(problems) && problems.map((problem) => (
            <TableRow key={problem.name} component={Link} to={`/problems/${problem.name}`} onClick={onClose} style={{ textDecoration: 'none' }}>
              <TableCell>{problem.title}</TableCell>
              <TableCell>{problem.description}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default ProblemList;
