import { List, ListItem, ListItemButton, ListItemText, Typography } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const ProblemListPage = () => {
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
        <div>
            <Typography variant="h4" gutterBottom>
                Problem List
            </Typography>
            <List>
                <ListItem>
                    <ListItemText primary="Title" />
                    <ListItemText primary="Point" />
                    <ListItemText primary="対応する回" />
                </ListItem>

                {Array.isArray(problems) && problems.map((problem) => (
                    <ListItem key={problem.name}>
                        <ListItemButton component={Link} to={`/problems/${problem.name}`}>
                            <ListItemText primary={problem.title} />
                            <ListItemText primary={problem.point} />
                            <ListItemText primary={problem.section} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </div>
    );
};

export default ProblemListPage;
