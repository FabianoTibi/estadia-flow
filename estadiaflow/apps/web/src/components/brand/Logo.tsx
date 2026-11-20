'use client';

import { useId } from 'react';
import styles from './logo.module.css';

/**
 * Marca EstadiaFlow. O desenho é o mesmo dos arquivos em public/brand
 * (gerados por scripts/build-brand.py); aqui ele fica inline para herdar tamanho e
 * não depender de uma requisição extra.
 */
export type LogoVariant = 'color' | 'navy' | 'white';

// Mesmo desenho de scripts/build-brand.py (caixa 64x64).
const ROOF = 'M16.5 26 L31 13 L41.4 22.3';
const BASE = 'M50 36.5 V50 a5 5 0 0 1 -5 5 H17 a5 5 0 0 1 -5 -5 V37.5';
const TAIL = 'M1 31 C11 29.5 22 30 29.2 35.2 L25.2 39.2 C20 34.5 11 32 1 31 Z';
const CHECK = 'M27 37 L35 45 L58 11';
const ROOF_REDUCED = 'M12 30 L31 13 L41.4 22.3';
const BASE_REDUCED = 'M50 37.5 V50 a5 5 0 0 1 -5 5 H17 a5 5 0 0 1 -5 -5 V30';
const CHECK_REDUCED = 'M26 36 L35 45 L58 11';
const CYAN = '#19C8F5';
const BLUE = '#2563EB';
const VIOLET = '#7C3AED';
const NAVY = '#0B1B4D';
const LIGHT_BLUE = '#7DB4FF';

interface LogoMarkProps {
  size?: number;
  /** color: fundo claro · white: fundo escuro (casa branca, check ciano) · navy: uma cor. */
  variant?: LogoVariant;
  /** Sem o rastro e com traço mais grosso: use abaixo de ~40 px. */
  reduced?: boolean;
  title?: string;
}

export function LogoMark({ size = 32, variant = 'color', reduced = false, title }: LogoMarkProps) {
  const uid = useId().replace(/[^a-zA-Z0-9]/g, '');
  const house = variant === 'color' ? `url(#${uid}h)` : variant === 'navy' ? NAVY : '#FFFFFF';
  const light = variant === 'navy' ? NAVY : `url(#${uid}s)`;
  const round = { strokeLinecap: 'round', strokeLinejoin: 'round' } as const;
  const width = reduced ? 7 : 5.5;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      role={title ? 'img' : undefined}
      aria-label={title}
      aria-hidden={title ? undefined : true}
      className={styles.mark}
    >
      {variant !== 'navy' && (
        <defs>
          {variant === 'color' && (
            <linearGradient id={`${uid}h`} x1="8" y1="12" x2="54" y2="58" gradientUnits="userSpaceOnUse">
              <stop offset="0" stopColor={NAVY} />
              <stop offset="0.55" stopColor={BLUE} />
              <stop offset="1" stopColor={VIOLET} />
            </linearGradient>
          )}
          <linearGradient id={`${uid}s`} x1="2" y1="40" x2="60" y2="8" gradientUnits="userSpaceOnUse">
            <stop offset="0" stopColor={CYAN} />
            <stop offset="1" stopColor={variant === 'color' ? BLUE : LIGHT_BLUE} />
          </linearGradient>
        </defs>
      )}
      <path d={reduced ? ROOF_REDUCED : ROOF} stroke={house} strokeWidth={width} {...round} />
      <path d={reduced ? BASE_REDUCED : BASE} stroke={house} strokeWidth={width} {...round} />
      {!reduced && <path d={TAIL} fill={light} />}
      <path d={reduced ? CHECK_REDUCED : CHECK} stroke={light} strokeWidth={width} {...round} />
    </svg>
  );
}

interface LogoProps {
  /** Altura do símbolo em px; o nome acompanha. */
  size?: number;
  variant?: LogoVariant;
  layout?: 'horizontal' | 'vertical';
  tagline?: boolean;
}

/** Assinatura completa: símbolo + "EstadiaFlow" (+ slogan opcional). */
export function Logo({ size = 36, variant = 'color', layout = 'horizontal', tagline = false }: LogoProps) {
  const reduced = size < 40;
  return (
    <span className={`${styles.logo} ${layout === 'vertical' ? styles.vertical : ''} ${variant === 'white' ? styles.onDark : ''}`}>
      <LogoMark size={size} variant={variant} reduced={reduced} />
      <span className={styles.text}>
        <span className={styles.word} style={{ fontSize: Math.round(size * (layout === 'vertical' ? 0.34 : 0.5)) }}>
          Estadia<span className={variant === 'color' ? styles.flow : variant === 'white' ? styles.flowDark : undefined}>Flow</span>
        </span>
        {tagline && <span className={styles.tagline}>Gerencie. Automatize. Encante.</span>}
      </span>
    </span>
  );
}
