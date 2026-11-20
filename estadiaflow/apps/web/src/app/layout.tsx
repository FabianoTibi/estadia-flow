import type { Metadata, Viewport } from 'next';
import type { ReactNode } from 'react';
import { AuthProvider } from '@/lib/auth';
// Fontes servidas pelo próprio aplicativo (sem requisições a terceiros).
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import '@fontsource/sora/600.css';
import '@fontsource/sora/700.css';
import '@fontsource/sora/800.css';
import '@/styles/globals.css';

// URL pública usada nos links absolutos (imagem de compartilhamento). Lida no build.
const siteUrl = process.env.WEB_URL ?? 'http://localhost:3000';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: { default: 'EstadiaFlow', template: '%s · EstadiaFlow' },
  applicationName: 'EstadiaFlow',
  appleWebApp: { capable: true, title: 'EstadiaFlow', statusBarStyle: 'default' },
  description: 'Gestão inteligente de hospedagens: reservas, limpeza, atendimento por WhatsApp e automações em um só lugar.',
  openGraph: {
    type: 'website',
    locale: 'pt_BR',
    siteName: 'EstadiaFlow',
    title: 'EstadiaFlow — Gerencie. Automatize. Encante.',
    description: 'Gestão inteligente de hospedagens: reservas, limpeza, atendimento por WhatsApp e automações em um só lugar.',
  },
  twitter: { card: 'summary_large_image', title: 'EstadiaFlow — Gerencie. Automatize. Encante.', description: 'Gestão inteligente de hospedagens: reservas, limpeza, atendimento por WhatsApp e automações em um só lugar.' },
  // Painel privado: páginas internas não devem ser indexadas por buscadores.
  robots: { index: false, follow: false },
};
export const viewport: Viewport = { width: 'device-width', initialScale: 1, themeColor: '#2563eb' };

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
