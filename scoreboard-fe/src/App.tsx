import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Link,
  List,
  ListItem,
  ListItemText,
  Box,
} from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import './App.css';
import AiBirrasLogo from './assets/AI-birras.png';
import QR from './assets/qr.png';

interface ToolScore {
  tool_name: string;
  description: string;
  website: string | null;
  reasons: string[];
  score: number;
}

interface ScoreboardResponse {
  top_tools: ToolScore[];
}

const theme = createTheme();

function App() {
  const [tools, setTools] = useState<ToolScore[]>([]);
  const [selectedTool, setSelectedTool] = useState<ToolScore | null>(null);
  const [updatedTools, setUpdatedTools] = useState<Set<string>>(new Set());
  const currentToolsRef = useRef<ToolScore[]>([]);

  useEffect(() => {
    const fetchScoreboard = async () => {
      try {
        const response = await axios.get<ScoreboardResponse>(`${import.meta.env.VITE_API_URL}/scoreboard/`);
        const newTools = response.data.top_tools;

        // Check for updates
        const updated = new Set<string>();
        newTools.forEach((newTool) => {
          const oldTool = currentToolsRef.current.find(t => t.tool_name === newTool.tool_name);
          if (oldTool && oldTool.score !== newTool.score) {
            updated.add(newTool.tool_name);
          }
        });

        setTools(newTools);
        currentToolsRef.current = newTools;

        // Only set updatedTools if there are actual changes
        if (updated.size > 0) {
          setUpdatedTools(updated);
          // Clear the updated class after animation
          setTimeout(() => setUpdatedTools(new Set()), 500);
        }
      } catch (error) {
        console.error('Error fetching scoreboard:', error);
      }
    };

    fetchScoreboard(); // Initial fetch
    const intervalId = setInterval(fetchScoreboard, 2000);
    return () => clearInterval(intervalId);
  }, []); // Empty dependency array

  const handleToolClick = (tool: ToolScore) => {
    setSelectedTool(tool);
  };

  const closeDialog = () => {
    setSelectedTool(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <Container maxWidth="lg">
        <Box display="flex" justifyContent="center" mb={4}>
          <img src={AiBirrasLogo} className='logo' />
        </Box>
        <Typography variant="h2" component="h1" gutterBottom align="center" sx={{ my: 4, color: "#666" }}>
          Top AI-Birras Tools Scoreboard
        </Typography>

        <Grid container spacing={3} sx={{ mb: 4, justifyContent: 'center' }}>
          {[1, 0, 2].map((index) => {
            const tool = tools[index];
            if (!tool) return null;
            return (
              <Grid item xs={12} sm={4} key={tool.tool_name} sx={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                order: { xs: index, sm: index === 0 ? 0 : index === 1 ? -1 : 1 }
              }}>
                <Card
                  onClick={() => handleToolClick(tool)}
                  className={updatedTools.has(tool.tool_name) ? 'updated' : ''}
                  sx={{
                    bgcolor: index === 0 ? 'gold' : index === 1 ? 'silver' : '#cd7f32',
                    '&:hover': { bgcolor: 'action.hover' },
                    width: '100%',
                    height: index === 0 ? 240 : index === 1 ? 200 : 160,
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    mb: index === 0 ? 0 : index === 1 ? 5 : 10
                  }}
                >
                  <CardActionArea>
                    <CardContent>
                      <Typography variant="h5" component="div" align="center">
                        {tool.tool_name}
                      </Typography>
                      <Typography variant="body2" align="center">
                        Score: {tool.score}
                      </Typography>
                    </CardContent>
                  </CardActionArea>
                </Card>
                <Typography variant="h4" sx={{ mt: 1 }}>
                  {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                </Typography>
              </Grid>
            );
          })}
        </Grid>

        <Grid container spacing={3} direction="column" alignItems="center" sx={{ mb: 4 }}>
          <Typography className="claim" variant='h3'>
            Entra en <span>https://duffbot.aibirras.org</span>
          </Typography>
          <Box display="flex" justifyContent="center" mt={2}>
            <img src={QR} className='qr' />
          </Box>
        </Grid>


        <Grid container spacing={2}>
          {tools.slice(3).map((tool, index) => (
            <Grid item xs={12} sm={6} md={4} lg={3} key={tool.tool_name}>
              <Card onClick={() => handleToolClick(tool)} className={updatedTools.has(tool.tool_name) ? 'updated' : ''}>
                <CardActionArea>
                  <CardContent>
                    <Typography variant="h6" component="div">
                      {tool.tool_name}
                    </Typography>
                    <Typography variant="body2">
                      Score: {tool.score}
                    </Typography>
                    <Typography variant="body2" sx={{ mt: 1 }}>
                      Rank: #{index + 4}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Dialog open={!!selectedTool} onClose={closeDialog} maxWidth="md" fullWidth>
          {selectedTool && (
            <>
              <DialogTitle>{selectedTool.tool_name}</DialogTitle>
              <DialogContent>
                <Typography variant="body1" paragraph>
                  {selectedTool.description}
                </Typography>
                {selectedTool.website && (
                  <Typography variant="body2" paragraph>
                    <Link href={selectedTool.website} target="_blank" rel="noopener noreferrer">
                      Visit Website
                    </Link>
                  </Typography>
                )}
                <Typography variant="h6" gutterBottom>
                  User Reasons:
                </Typography>
                <List>
                  {selectedTool.reasons.map((reason, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={
                          <Typography variant="body2" component="blockquote" sx={{
                            borderLeft: '5px solid #ccc',
                            pl: 2,
                            py: 1,
                            fontStyle: 'italic'
                          }}>
                            "{reason}"
                          </Typography>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </DialogContent>
              <DialogActions>
                <Button onClick={closeDialog}>Close</Button>
              </DialogActions>
            </>
          )}
        </Dialog>
      </Container>
    </ThemeProvider>
  );
}

export default App;
