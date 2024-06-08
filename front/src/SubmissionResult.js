import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Container, Typography, Box } from '@mui/material';

const SubmissionResult = () => {
  const { taskId } = useParams();
  const [submissionResult, setSubmissionResult] = useState(null);

  useEffect(() => {
    const fetchResult = async (taskId) => {
      try {
        const resultResponse = await axios.get(`http://localhost:8000/result/${taskId}`);
        if (resultResponse.data.status === "Completed") {
          console.log("Result:", resultResponse.data.result);
          setSubmissionResult(resultResponse.data.result);
        } else if (resultResponse.data.status === "Pending") {
          console.log("Result is still pending...");
          setTimeout(() => fetchResult(taskId), 2000); // 2秒後に再度リクエスト
        }
      } catch (error) {
        console.error("There was an error fetching the result!", error);
      }
    };

    fetchResult(taskId);
  }, [taskId]);

  return (
    <Container maxWidth="md" style={{ marginTop: '50px', backgroundColor: '#f5f5f5', padding: '20px', borderRadius: '8px' }}>
      <Typography variant="h6" gutterBottom>Submission Result</Typography>
      {submissionResult ? (
        <Box p={2} bgcolor="#e0f7fa" borderRadius="8px">
          <Typography variant="body1">Status: {submissionResult.status}</Typography>
          <Typography variant="body1">Execution Time: {submissionResult.time} seconds</Typography>
          <Typography variant="body1">Memory Used: {submissionResult.memory} MB</Typography>
          <Typography variant="body1">Output:</Typography>
          <pre>{submissionResult.stdout}</pre>
          {submissionResult.stderr && (
            <>
              <Typography variant="body1">Errors:</Typography>
              <pre>{submissionResult.stderr}</pre>
            </>
          )}
        </Box>
      ) : (
        <Typography variant="body1">Loading...</Typography>
      )}
    </Container>
  );
};

export default SubmissionResult;
