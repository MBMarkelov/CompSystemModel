import React, { useState, useEffect, useRef } from "react";
import { Box, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();  
  const toggleSpawning = () => {
    setIsSpawning((prev) => !prev);
  };

  return (
    <Box position="relative" minHeight="100vh" sx={{ bgcolor: "#f5f5f5" }}>
      <Box
        position="absolute"
        top={10}
        left="50%"
        sx={{ transform: "translateX(-50%)", zIndex: 10 }}
      >
      </Box>

      {/* Основной контент страницы */}
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        minHeight="100vh"
      >
        <Typography variant="h3" mb={5} textAlign="center" sx={{ color: "black" }}>
          "Компьютерные системы моделирования"
        </Typography>
        <Box display="flex" gap={2}>
          {[1, 2, 3, 4, 5, 6].map((lab) => (
            <Button
              key={lab}
              variant="contained"
              onClick={() => navigate(`/lab${lab}`)}
              sx={{ fontSize: "18px", padding: "10px 20px" }}
            >
              Лабораторная {lab}
            </Button>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Home;
