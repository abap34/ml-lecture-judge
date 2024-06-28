import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';

const getRandomColor = () => {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
};

const ProblemListPage = () => {
    const [problems, setProblems] = useState([]);
    const [sectionColors, setSectionColors] = useState({});

    useEffect(() => {
        const fetchProblems = async () => {
            try {
                const response = await axios.get(`${process.env.REACT_APP_API_URL}/problems`, { withCredentials: true });
                const problemsData = response.data;

                const problemsWithSolvedCount = await Promise.all(problemsData.map(async (problem) => {
                    const solvedUserCountResponse = await axios.get(`${process.env.REACT_APP_API_URL}/problems/${problem.name}/solved_user_count`, { withCredentials: true });
                    return { ...problem, solvedUserCount: solvedUserCountResponse.data.count };
                }));

                const newSectionColors = {};
                problemsWithSolvedCount.forEach((problem) => {
                    if (!newSectionColors[problem.section]) {
                        newSectionColors[problem.section] = getRandomColor();
                    }
                });

                setProblems(problemsWithSolvedCount);
                setSectionColors(newSectionColors);
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
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <TableCell>問題</TableCell>
                            <TableCell>得点</TableCell>
                            <TableCell>対応する回</TableCell>
                            <TableCell>解いた人数</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {problems.map((problem) => (
                            <TableRow key={problem.name} component={Link} to={`/problems/${problem.name}`} style={{ textDecoration: 'none' }}>
                                <TableCell style={{ borderLeft: `8px solid ${sectionColors[problem.section]}` }}></TableCell>
                                <TableCell>{problem.title}</TableCell>
                                <TableCell>{problem.point}</TableCell>
                                <TableCell>{problem.section}</TableCell>
                                <TableCell>{problem.solvedUserCount}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};

export default ProblemListPage;
