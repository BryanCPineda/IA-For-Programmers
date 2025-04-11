import Image from "next/image"
import Link from "next/link"
import { ChevronDown, MonitorSmartphone, BookOpen, Users, Shield } from "lucide-react"

export default function Home() {
  return (
    <main className="min-h-screen">
      {/* Header */}
      <header className="container mx-auto flex items-center justify-between py-6 px-4">
        <div className="flex items-center">
          <Link href="/" className="font-bold text-2xl">
            <Image src="/logo-henry.png" alt="HENRY" width={120} height={40} className="h-6" />
          </Link>
        </div>
        <div className="flex items-center space-x-6">
          <div className="flex items-center">
            <button className="flex items-center text-gray-700 font-medium">
              Para estudiantes
              <ChevronDown className="ml-1 h-4 w-4" />
            </button>
          </div>
          <div className="flex items-center">
            <button className="flex items-center text-gray-700 font-medium">
              Para empresas
              <ChevronDown className="ml-1 h-4 w-4" />
            </button>
          </div>
          <Link href="/ingresar" className="text-gray-700 font-medium">
            Ingresar
          </Link>
          <Link
            href="/aplicar"
            className="bg-yellow-400 hover:bg-yellow-500 text-black font-medium px-6 py-2 rounded-md"
          >
            Aplicar
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-12 md:py-20">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight">
              Comienza o acelera tu carrera en tecnología
            </h1>
            <h2 className="text-xl md:text-2xl font-medium">
              Estudia Desarrollo Full Stack, Data Science o Data Analytics.
            </h2>

            <div className="space-y-4 pt-4">
              <div className="flex items-center">
                <MonitorSmartphone className="h-6 w-6 text-purple-600 mr-3" />
                <span>Online, en vivo y flexible</span>
              </div>
              <div className="flex items-center">
                <BookOpen className="h-6 w-6 text-purple-600 mr-3" />
                <span>Basado en proyectos</span>
              </div>
              <div className="flex items-center">
                <Users className="h-6 w-6 text-purple-600 mr-3" />
                <span>Basado en cohortes</span>
              </div>
              <div className="flex items-center">
                <Shield className="h-6 w-6 text-purple-600 mr-3" />
                <span>Garantía de Empleo</span>
              </div>
            </div>

            <div className="pt-4">
              <Link
                href="/aplicar"
                className="inline-block bg-yellow-400 hover:bg-yellow-500 text-black font-medium px-8 py-3 rounded-md"
              >
                Aplicar
              </Link>
            </div>
          </div>

          <div className="relative">
            <Image
              src="/placeholder.webp"
              alt="Estudiante de programación"
              width={600}
              height={600}
              className="rounded-lg"
            />
          </div>
        </div>
      </section>

      {/* Footer Banner */}
      <section className="py-12 text-center">
        <h3 className="text-2xl font-bold">
          Bootcamp <span className="text-purple-600">#1</span> de Latam
        </h3>
      </section>
    </main>
  )
}
