import { List, ListItem, ListItemButton, ListItemText } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

function ProblemList({ onClose }) {
  const [problems, setProblems] = useState([]);

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

export default ProblemList;
