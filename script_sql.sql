CREATE TABLE IF NOT EXISTS previsao_tempo (
  id SERIAL PRIMARY KEY,
  cidade TEXT NOT NULL,
  data_previsao DATE NOT NULL,
  temp_media DECIMAL(5,2) NOT NULL,
  tem_chuva BOOLEAN NOT NULL,
  indice_conforto TEXT NOT NULL,
  criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);