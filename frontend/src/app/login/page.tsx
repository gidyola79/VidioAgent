"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Loader2, Unlock, Eye, EyeOff } from "lucide-react"
import { setAuthToken } from "@/lib/api"
import { useRouter } from "next/navigation"

export default function LoginPage(){
    const router = useRouter()
    const [phone, setPhone] = useState("")
    const [password, setPassword] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [showPassword, setShowPassword] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setError("")

        if (!phone || !password) {
            setError("Please provide both phone number and password")
            return
        }

        setLoading(true)
            try {
                const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
                const res = await fetch(`${API_URL}/api/auth/login`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ phone, password })
                })

                if (!res.ok) {
                    const data = await res.json().catch(() => ({}))
                    throw new Error(data.detail || "Login failed")
                }

                const data = await res.json()
                const token = data.access_token
                if (token) {
                    setAuthToken(token)
                }

                router.push("/")
            } catch (err: any) {
                setError(err.message || "Login error")
            } finally {
                setLoading(false)
            }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
            <div className="w-full max-w-md px-4">
                <Card className="w-full shadow-2xl">
                    <CardHeader>
                        <CardTitle className="text-2xl">Sign In</CardTitle>
                        <CardDescription>Access your business account</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-sm font-medium">WhatsApp Number</label>
                                <Input
                                    placeholder="+2348012345678"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    required
                                    inputMode="tel"
                                    aria-label="WhatsApp number"
                                />
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium">Password</label>
                                <div className="relative">
                                    <Input type={showPassword ? "text" : "password"} placeholder="Your account password" value={password} onChange={(e) => setPassword(e.target.value)} required />
                                    <button type="button" onClick={() => setShowPassword((s) => !s)} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700" aria-label={showPassword ? "Hide password" : "Show password"}>
                                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                    </button>
                                </div>
                            </div>

                            {error && <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">{error}</div>}

                            <div className="flex items-center justify-between gap-4">
                                <div className="flex items-center gap-3">
                                    <input id="remember" type="checkbox" className="w-4 h-4" />
                                    <label htmlFor="remember" className="text-sm text-muted-foreground">Remember me</label>
                                </div>
                                <a href="#" className="text-sm text-blue-600 hover:underline">Forgot password?</a>
                            </div>

                            <Button type="submit" className="w-full py-3 text-base bg-gradient-to-r from-purple-600 to-blue-600" disabled={loading}>
                                {loading ? <><Loader2 className="mr-2 h-4 w-4 animate-spin"/> Signing in...</> : <><Unlock className="mr-2 h-4 w-4"/> Sign In</>}
                            </Button>

                            <p className="text-center text-sm text-muted-foreground mt-2">Don't have an account? <a href="/register" className="text-blue-600 hover:underline">Register</a></p>
                        </form>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
