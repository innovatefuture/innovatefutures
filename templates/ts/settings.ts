export interface Settings {
    MAPTILER_API_KEY: string
}

// window.settings is set in base.html
// @ts-expect-error
const settings = (window.settings ?? {}) as Settings

export const MAPTILER_API_KEY = settings.MAPTILER_API_KEY
export const MAPTILER_STYLE_URL = `https://api.maptiler.com/maps/57b72401-25b7-4966-ace2-092c984f2e0b/style.json?key=${MAPTILER_API_KEY}`