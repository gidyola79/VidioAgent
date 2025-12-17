"use client"

import React from "react"
import Link from "next/link"
import { isAuthenticated, logout } from "@/lib/auth"

export default function AuthHeader() {
    const [authed, setAuthed] = React.useState(false)

    React.useEffect(() => {
        setAuthed(isAuthenticated())
    }, [])

    const handleLogout = () => {
        logout()
        setAuthed(false)
        // reload or navigate to home
        window.location.href = "/"
    }

    return (
        <header className="w-full py-3 border-b bg-white/50 dark:bg-slate-900/50">
            <div className="container mx-auto px-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/" className="font-bold text-lg text-slate-900 dark:text-white">VidioAgent</Link>
                </div>
                <nav>
                    {authed ? (
                        <div className="flex items-center gap-3">
                            <button onClick={handleLogout} className="px-3 py-2 bg-red-600 text-white rounded-md">Logout</button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-3">
                            <Link href="/login" className="px-3 py-2 bg-blue-600 text-white rounded-md">Sign In</Link>
                            <Link href="/register" className="px-3 py-2 border rounded-md">Register</Link>
                        </div>
                    )}
                </nav>
            </div>
        </header>
    )
}
