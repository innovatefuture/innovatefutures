export interface Settings {
    MAPTILER_API_KEY: string
}

// window.settings is set in base.html
// @ts-expect-error
const settings = (window.settings ?? {}) as Settings

export const MAPTILER_API_KEY = settings.MAPTILER_API_KEY
export const MAPTILER_STYLE_URL = `https://api.maptiler.com/maps/1bdae867-4b62-4fcd-9410-c1fccc3fc6b6/style.json?key=${MAPTILER_API_KEY}`