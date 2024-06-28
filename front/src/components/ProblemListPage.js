import React, { useEffect, useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography, Paper } from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';

const sectionColors = {
    "0": "#FFEBE5",
    "1": "#E5FFEB",
    "2": "#E5EBFF",
    "3": "#FFE5F2",
    "4": "#E5FFF7",
    "5": "#FFFCE5",
    "6": "#F2E5FF",
    "7": "#FFEDCC"
};

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
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell></TableCell>
                            <TableCell>対応する回</TableCell>
                            <TableCell>問題</TableCell>
                            <TableCell>得点</TableCell>
                            <TableCell>解いた人数</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {problems.map((problem) => (
                            <TableRow key={problem.name} component={Link} to={`/problems/${problem.name}`} style={{ textDecoration: 'none' }}>
                                <TableCell style={{ borderLeft: `8px solid ${sectionColors[problem.section]}` }}></TableCell>
                                <TableCell>{problem.section}</TableCell>
                                <TableCell>{problem.title}</TableCell>
                                <TableCell>{problem.point}</TableCell>
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
