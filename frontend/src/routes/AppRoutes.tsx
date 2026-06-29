import { BrowserRouter, Navigate, Route, Routes } from 'react-router';

import AppLayout from '~/components/layout/AppLayout';
import Dashboard from '~/pages/Dashboard/Dashboard';
import { ROUTES } from '~/routes/paths';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route path={ROUTES.root} element={<Dashboard />} />

          <Route path={ROUTES.fallback} element={<Navigate to={ROUTES.root} replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
