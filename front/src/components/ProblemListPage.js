import { List, ListItem, ListItemButton, ListItemText, Typography, Grid } from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const ProblemListPage = () => {
    const [problems, setProblems] = useState([]);

    useEffect(() => {
        const fetchProblems = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}/problems`, { withCredentials: true });
                const problemsData = response.data;

                const problemsWithSolvedCount = await Promise.all(problemsData.map(async (problem) => {
                    const solvedUserCountResponse = await axios.get(`${process.env.REACT_APP_API_URL}/problems/${problem.name}/solved_user_count`, { withCredentials: true });
                    return { ...problem, solvedUserCount: solvedUserCountResponse.data.count };
                }));

                setProblems(problemsWithSolvedCount);
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
                    <Grid container spacing={2}>
                        <Grid item xs={3}>
                            <ListItemText primary="Title" />
                        </Grid>
                        <Grid item xs={2}>
                            <ListItemText primary="Point" />
                        </Grid>
                        <Grid item xs={2}>
                            <ListItemText primary="対応する回" />
                        </Grid>
                        <Grid item xs={2}>
                            <ListItemText primary="Solved User Count" />
                        </Grid>
                    </Grid>
                </ListItem>

                {Array.isArray(problems) && problems.map((problem) => (
                    <ListItem key={problem.name}>
                        <ListItemButton component={Link} to={`/problems/${problem.name}`}>
                            <Grid container spacing={2}>
                                <Grid item xs={3}>
                                    <ListItemText primary={problem.title} />
                                </Grid>
                                <Grid item xs={2}>
                                    <ListItemText primary={problem.point} />
                                </Grid>
                                <Grid item xs={2}>
                                    <ListItemText primary={problem.section} />
                                </Grid>
                                <Grid item xs={2}>
                                    <ListItemText primary={problem.solvedUserCount} />
                                </Grid>
                            </Grid>
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
        </div>
    );
};

export default ProblemListPage;
