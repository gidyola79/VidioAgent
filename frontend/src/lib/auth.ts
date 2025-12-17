"use client"

import { setAuthToken } from "./api"

export function getToken(): string | null {
    try { return localStorage.getItem('vidioagent_token') } catch { return null }
}

export function isAuthenticated(): boolean {
    const t = getToken()
    return !!t
}

export function logout(): void {
    try { setAuthToken(null) } catch {}
}
