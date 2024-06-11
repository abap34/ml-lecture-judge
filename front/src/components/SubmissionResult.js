import React, { useEffect, useState, useRef } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Container, Typography, Box, Paper, Table, TableBody, TableCell, TableContainer, TableRow, Chip, Tab } from '@mui/material';
import { useCodeMirror } from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';

const SubmissionResult = () => {
  const { taskId } = useParams();
  const [submissionResult, setSubmissionResult] = useState(null);
  const editor = useRef(null);

  useEffect(() => {
    const fetchResult = async (taskId) => {
      try {
        const resultResponse = await axios.get(`http://localhost:8000/result/${taskId}`);
        if (resultResponse.data.status === "Completed") {
          setSubmissionResult(resultResponse.data.result);
        } else if (resultResponse.data.status === "Pending") {
          setTimeout(() => fetchResult(taskId), 2000); // 2秒後に再度リクエスト
        }
      } catch (error) {
        console.error("There was an error fetching the result!", error);
      }
    };

    fetchResult(taskId);
  }, [taskId]);

  const { setContainer } = useCodeMirror({
    container: editor.current,
    extensions: [python()],
    value: submissionResult ? submissionResult.code : '',
    options: {
      readOnly: true,
      lineNumbers: true,
      lineWrapping: true,
      theme: 'light',
    },
  });

  useEffect(() => {
    if (editor.current) {
      setContainer(editor.current);
    }
  }, [setContainer, submissionResult]);

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
        Submission Result
      </Typography>
      {submissionResult ? (
        <>
          <Box p={2} mb={4} component={Paper}>
            <Typography variant="h6" gutterBottom>Submitted Code</Typography>
            <div ref={editor} style={{ border: '1px solid #ddd', borderRadius: '4px', height: '400px', overflow: 'auto' }}></div>
          </Box>
          <Box p={2} component={Paper}>
            <Typography variant="h6" gutterBottom>Result Details</Typography>
            <TableContainer>
              <Table>
                <TableBody>
                  <TableRow>
                    <TableCell><strong>Problem</strong></TableCell>
                    <TableCell><a href={`/problems/${submissionResult.problem_name}`}>{submissionResult.problem_name}</a></TableCell>
                    </TableRow>
                  <TableRow>
                    <TableCell><strong>Status</strong></TableCell>
                    <TableCell>
                      <Chip
                        label={submissionResult.status}
                        color={getStatusColor(submissionResult.status)}
                      />
                    </TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><strong>Execution Time</strong></TableCell>
                    <TableCell>{submissionResult.execution_time} seconds</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><strong>Submitted At</strong></TableCell>
                    <TableCell>{new Date(submissionResult.submitted_at).toLocaleString()}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell><strong>Test Cases</strong></TableCell>
                    <TableCell>{submissionResult.passed_cases}/{submissionResult.n_testcases}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        </>
      ) : (
        <Typography variant="body1">Loading result...</Typography>
      )}
    </Container>
  );
};

export default SubmissionResult;