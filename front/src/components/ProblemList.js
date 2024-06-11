import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, ListItemButton } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';

function ProblemList({ onClose }) {
  const [problems, setProblems] = useState([]);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const response = await axios.get('http://localhost:8000/problems');
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
