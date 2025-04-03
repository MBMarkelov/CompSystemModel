import React, { useState } from "react";
import { Button, Box, Typography, CircularProgress, Modal, Paper } from "@mui/material";

const Lab4 = () => {
  const [openModal, setOpenModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [plots, setPlots] = useState(null);

  const handleOpenModal = () => {
    setOpenModal(true);
  };

  const handleCloseModal = () => {
    setOpenModal(false);
    setPlots(null);
  };

  const fetchPlots = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/L4/frequensy_tests/");
      if (!response.ok) {
        throw new Error("Ошибка при загрузке графиков");
      }
      const data = await response.json();
      setPlots(data);
      handleOpenModal();
    } catch (error) {
      console.error("Ошибка при загрузке графиков:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
      }}
    >
      <Typography variant="h4" gutterBottom>
        Лабораторная работа 4: Частотные тесты генераторов
      </Typography>

      <Button
        variant="contained"
        color="primary"
        onClick={fetchPlots}
        sx={{ marginBottom: 2 }}
      >
        Получить графики
      </Button>

      {loading && <CircularProgress sx={{ marginTop: 2 }} />}

      <Modal open={openModal} onClose={handleCloseModal}>
        <Paper
          sx={{
            position: "absolute",
            top: 0,
            left: "50%",
            transform: "translateX(-50%)",
            width: "90%",
            maxWidth: 900,
            padding: 2,
            outline: "none",
            overflowY: "auto",
            maxHeight: "100vh",
          }}
        >
          <Typography variant="h6" gutterBottom>
            Графики частотного теста
          </Typography>
          {plots && (
            <Box>
              <Typography variant="subtitle1">Мультиномиальный генератор</Typography>
              <img
                src={`data:image/png;base64,${plots.multinomial_plot}`}
                alt="Multinomial Plot"
                style={{ maxWidth: "100%", marginBottom: "20px" }}
              />
              <Typography variant="subtitle1">Кубический конгруэнтный генератор</Typography>
              <img
                src={`data:image/png;base64,${plots.cubic_plot}`}
                alt="Cubic Plot"
                style={{ maxWidth: "100%" }}
              />
            </Box>
          )}
          <Button onClick={handleCloseModal} variant="contained" sx={{ marginTop: 2 }}>
            Закрыть
          </Button>
        </Paper>
      </Modal>

    </Box>
  );
};

export default Lab4;
