import { BrowserRouter, Navigate, Route, Routes } from 'react-router';

import AppLayout from '~/components/layout/AppLayout';
import CurrentElection from '~/pages/CurrentElection';
import HistoricalElections from '~/pages/HistoricalElections';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path="/" element={<Navigate to="/current-election" replace />} />

          <Route path="/current-election" element={<CurrentElection />} />

          <Route path="/historical-elections" element={<HistoricalElections />} />

          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
