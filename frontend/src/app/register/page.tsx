"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ThemeToggle } from "@/components/theme-toggle"
import { Loader2, Sparkles, Upload, CheckCircle, Eye, EyeOff } from "lucide-react"
import { useRouter } from "next/navigation"

export default function RegisterPage() {
    const router = useRouter()
    const [formData, setFormData] = useState({
        name: "",
        whatsapp_number: "",
        owner_name: "",
        business_type: "",
        response_style: "professional",
        password: ""
    })
    const [voiceSample, setVoiceSample] = useState<File | null>(null)
    const [avatarImage, setAvatarImage] = useState<File | null>(null)
    const [avatarPreview, setAvatarPreview] = useState<string | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")
    const [success, setSuccess] = useState(false)
    const [showPassword, setShowPassword] = useState(false)

    useEffect(() => {
        // cleanup object URL when component unmounts or image changes
        return () => {
            if (avatarPreview) URL.revokeObjectURL(avatarPreview)
        }
    }, [avatarPreview])

    // Drag & drop helpers (simple)
    const handleDropFile = (e: React.DragEvent, type: "voice" | "avatar") => {
        e.preventDefault()
        const f = e.dataTransfer.files?.[0] || null
        if (!f) return
        if (type === "voice") setVoiceSample(f)
        if (type === "avatar") {
            setAvatarImage(f)
            setAvatarPreview(URL.createObjectURL(f))
        }
    }

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault()
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        if (!voiceSample || !avatarImage) {
            setError("Please upload both voice sample and avatar image")
            return
        }

        if (!formData.password || formData.password.length < 8) {
            setError("Please provide a password (minimum 8 characters)")
            return
        }

        setLoading(true)
        setError("")

        try {
            const formDataToSend = new FormData()
            formDataToSend.append("name", formData.name)
            formDataToSend.append("whatsapp_number", formData.whatsapp_number)
            formDataToSend.append("owner_name", formData.owner_name)
            formDataToSend.append("business_type", formData.business_type)
            formDataToSend.append("response_style", formData.response_style)
            formDataToSend.append("password", formData.password)
            formDataToSend.append("voice_sample", voiceSample)
            formDataToSend.append("avatar_image", avatarImage)

            const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"
            const response = await fetch(`${API_URL}/api/business/register`, {
                method: "POST",
                body: formDataToSend,
            })

            if (!response.ok) {
                const errorData = await response.json()
                throw new Error(errorData.detail || "Registration failed")
            }

            const result = await response.json()
            setSuccess(true)

            // Redirect to home after 3 seconds
            setTimeout(() => {
                router.push("/")
            }, 3000)
        } catch (err: any) {
            setError(err.message || "Failed to register business")
        } finally {
            setLoading(false)
        }
    }

    const getPasswordStrength = (pw: string) => {
        if (!pw) return { label: "", percent: 0 }
        let score = 0
        if (pw.length >= 8) score += 1
        if (/[A-Z]/.test(pw)) score += 1
        if (/[0-9]/.test(pw)) score += 1
        if (/[^A-Za-z0-9]/.test(pw)) score += 1
        const percent = Math.min(100, Math.round((score / 4) * 100))
            const label = score <= 1 ? "Weak" : score === 2 ? "Fair" : score === 3 ? "Good" : "Strong"
            return { label, percent }
    }

    if (success) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
                <Card className="max-w-md w-full shadow-2xl">
                    <CardContent className="pt-6">
                        <div className="text-center space-y-4">
                            <CheckCircle className="w-16 h-16 text-green-500 mx-auto" />
                            <h2 className="text-2xl font-bold">Registration Successful!</h2>
                            <p className="text-muted-foreground">
                                Your business has been registered. You can now receive AI video responses on WhatsApp!
                            </p>
                            <p className="text-sm text-muted-foreground">Redirecting to home...</p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
            <div className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-600 to-blue-600 flex items-center justify-center">
                            <Sparkles className="w-7 h-7 text-white" />
                        </div>
                        <div>
                            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
                                VidioAgent
                            </h1>
                            <p className="text-sm text-muted-foreground">Business Registration</p>
                        </div>
                    </div>
                    <ThemeToggle />
                </div>

                {/* Registration Form */}
                <div className="max-w-4xl mx-auto px-4">
                    <Card className="shadow-xl border-purple-100 dark:border-purple-900">
                        <CardHeader>
                            <CardTitle className="text-2xl">Register Your Business</CardTitle>
                            <CardDescription>
                                Set up AI-powered video responses for your WhatsApp Business account
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div className="space-y-4">
                                    <h3 className="font-semibold text-lg">Business Information</h3>

                                    <div className="space-y-2">
                                        <label htmlFor="name" className="text-sm font-medium">
                                            Business Name <span className="text-destructive">*</span>
                                        </label>
                                        <Input
                                            id="name"
                                            placeholder="e.g., Ada's Bakery"
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                            required
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <label htmlFor="whatsapp" className="text-sm font-medium">
                                            WhatsApp Business Number <span className="text-destructive">*</span>
                                        </label>
                                        <Input
                                            id="whatsapp"
                                            placeholder="+234 801 234 5678"
                                            value={formData.whatsapp_number}
                                            onChange={(e) => setFormData({ ...formData, whatsapp_number: e.target.value })}
                                            required
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <label htmlFor="owner" className="text-sm font-medium">
                                            Owner Name <span className="text-destructive">*</span>
                                        </label>
                                        <Input
                                            id="owner"
                                            placeholder="Your name"
                                            value={formData.owner_name}
                                            onChange={(e) => setFormData({ ...formData, owner_name: e.target.value })}
                                            required
                                        />
                                    </div>

                                    <div className="space-y-2">
                                        <label htmlFor="password" className="text-sm font-medium">
                                            Account Password <span className="text-destructive">*</span>
                                        </label>
                                        <div className="relative">
                                            <Input
                                                id="password"
                                                type={showPassword ? "text" : "password"}
                                                placeholder="Choose a password (min 8 chars)"
                                                value={formData.password}
                                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                                required
                                            />
                                            <button
                                                type="button"
                                                onClick={() => setShowPassword((s) => !s)}
                                                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-700"
                                                aria-label={showPassword ? "Hide password" : "Show password"}
                                            >
                                                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                                            </button>
                                        </div>
                                        <p className="text-xs text-muted-foreground">
                                            You'll use this password to sign in as the business owner
                                        </p>

                                        {formData.password && (
                                            <div className="mt-2">
                                                <div className="h-2 w-full bg-slate-200 rounded overflow-hidden">
                                                    <div
                                                        style={{ width: `${getPasswordStrength(formData.password).percent}%` }}
                                                        className="h-2 bg-gradient-to-r from-red-500 via-yellow-400 to-green-500"
                                                    />
                                                </div>
                                                <p className="text-xs mt-1 text-muted-foreground">
                                                    {getPasswordStrength(formData.password).label}
                                                </p>
                                            </div>
                                        )}
                                    </div>

                                    <div className="space-y-2">
                                        <label htmlFor="type" className="text-sm font-medium">
                                            Business Type <span className="text-destructive">*</span>
                                        </label>
                                        <Input
                                            id="type"
                                            placeholder="e.g., Bakery, Salon, Restaurant"
                                            value={formData.business_type}
                                            onChange={(e) => setFormData({ ...formData, business_type: e.target.value })}
                                            required
                                        />
                                    </div>
                                </div>

                                {/* File Uploads */}
                                <div className="space-y-4 md:col-span-1">
                                    <h3 className="font-semibold text-lg">Media Assets</h3>

                                    <div className="space-y-2">
                                        <label htmlFor="voice" className="text-sm font-medium">
                                            Voice Sample <span className="text-destructive">*</span>
                                        </label>
                                        <div
                                            onDragOver={handleDragOver}
                                            onDrop={(e) => handleDropFile(e, "voice")}
                                            className="flex flex-col sm:flex-row items-center gap-3 p-3 border border-dashed rounded-md hover:border-slate-400"
                                        >
                                            <Input
                                                id="voice"
                                                type="file"
                                                accept="audio/*"
                                                onChange={(e) => setVoiceSample(e.target.files?.[0] || null)}
                                                required
                                                className="w-full sm:w-auto"
                                            />
                                            <div className="text-sm text-muted-foreground">
                                                <div>{voiceSample ? voiceSample.name : "Drag & drop a file or browse"}</div>
                                                {voiceSample && <div className="text-xs">{Math.round(voiceSample.size / 1024)} KB</div>}
                                            </div>
                                        </div>
                                        <p className="text-xs text-muted-foreground">
                                            Upload a 10-30 second audio clip of your voice (drag & drop supported)
                                        </p>
                                    </div>

                                    <div className="space-y-2">
                                        <label htmlFor="avatar" className="text-sm font-medium">
                                            Avatar Image <span className="text-destructive">*</span>
                                        </label>
                                        <div
                                            onDragOver={handleDragOver}
                                            onDrop={(e) => handleDropFile(e, "avatar")}
                                            className="flex flex-col sm:flex-row items-center gap-3 p-3 border border-dashed rounded-md hover:border-slate-400"
                                        >
                                            <Input
                                                id="avatar"
                                                type="file"
                                                accept="image/*"
                                                onChange={(e) => {
                                                    const f = e.target.files?.[0] || null
                                                    setAvatarImage(f)
                                                    if (f) {
                                                        const url = URL.createObjectURL(f)
                                                        setAvatarPreview(url)
                                                    } else {
                                                        setAvatarPreview(null)
                                                    }
                                                }}
                                                required
                                                className="w-full sm:w-auto"
                                            />
                                            <div className="flex items-center gap-3">
                                                {avatarPreview ? (
                                                    <img src={avatarPreview} alt="avatar preview" className="w-20 h-20 rounded-md object-cover border" />
                                                ) : (
                                                    <div className="w-20 h-20 bg-slate-100 rounded-md flex items-center justify-center text-sm text-muted-foreground">Preview</div>
                                                )}
                                            </div>
                                        </div>
                                        <p className="text-xs text-muted-foreground">
                                            Upload a clear photo of yourself for video generation
                                        </p>
                                    </div>
                                </div>

                                {error && (
                                    <div className="p-3 rounded-lg bg-destructive/10 text-destructive text-sm">
                                        {error}
                                    </div>
                                )}

                                <Button
                                    type="submit"
                                    disabled={loading}
                                    className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                                    size="lg"
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                                            Registering...
                                        </>
                                    ) : (
                                        <>
                                            <Sparkles className="mr-2 h-4 w-4" />
                                            Register Business
                                        </>
                                    )}
                                </Button>
                            </form>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
