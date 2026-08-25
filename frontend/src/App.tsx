import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClientProvider } from "@tanstack/react-query";
import { queryClient } from "./lib/query-client";
import { AppShell } from "./components/layout/AppShell";
import { ProjectsListPage } from "./features/projects/ProjectsListPage";
import { ProjectDetailPage } from "./features/projects/ProjectDetailPage";
import { QuantitySurveyPage } from "./features/quantity-survey/QuantitySurveyPage";
import { DevisPage } from "./features/pricing/DevisPage";
import { PriceCatalogPage } from "./features/pricing/PriceCatalogPage";

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AppShell>
          <Routes>
            <Route path="/" element={<ProjectsListPage />} />
            <Route path="/projects/:projectId" element={<ProjectDetailPage />} />
            <Route path="/plans/:planId/metre" element={<QuantitySurveyPage />} />
            <Route path="/plans/:planId/devis" element={<DevisPage />} />
            <Route path="/catalogue" element={<PriceCatalogPage />} />
          </Routes>
        </AppShell>
      </BrowserRouter>
    </QueryClientProvider>
  );
}