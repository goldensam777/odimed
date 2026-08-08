import { Appearance } from "@/components/Common/Appearance"
import { Logo } from "@/components/Common/Logo"
import { Footer } from "./Footer"

interface AuthLayoutProps {
  children: React.ReactNode
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="relative hidden lg:flex lg:flex-col lg:justify-between bg-zinc-950 p-12 overflow-hidden border-r border-border">
        {/* Background Gradients */}
        <div className="absolute inset-0 bg-gradient-to-br from-emerald-900/20 via-teal-900/20 to-zinc-950 z-0" />
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-[radial-gradient(ellipse_at_top_left,_var(--tw-gradient-stops))] from-teal-500/20 via-transparent to-transparent z-0 blur-3xl" />
        <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-[radial-gradient(ellipse_at_bottom_right,_var(--tw-gradient-stops))] from-emerald-500/10 via-transparent to-transparent z-0 blur-3xl" />

        <div className="relative z-10 flex justify-start">
          <Logo
            variant="full"
            className="scale-125 origin-left"
            asLink={false}
          />
        </div>

        <div className="relative z-10 flex flex-col gap-8 max-w-lg mb-12">
          <div className="space-y-4">
            <h1 className="text-4xl font-semibold tracking-tight text-white leading-tight">
              L'avenir de la <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-emerald-400">
                prescription médicale.
              </span>
            </h1>
            <p className="text-zinc-400 text-lg leading-relaxed">
              Odimed permet aux médecins de numériser leurs ordonnances en
              conservant leur identité visuelle. Signatures, cachets et suivi
              patient dans un même écosystème sécurisé.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-4 mt-4">
            <div className="bg-white/5 border border-white/10 p-5 rounded-2xl backdrop-blur-md shadow-2xl">
              <h3 className="font-semibold text-emerald-400 mb-1.5 flex items-center gap-2">
                ⚡ Gain de temps
              </h3>
              <p className="text-sm text-zinc-400">
                Générez vos documents certifiés en quelques clics.
              </p>
            </div>
            <div className="bg-white/5 border border-white/10 p-5 rounded-2xl backdrop-blur-md shadow-2xl">
              <h3 className="font-semibold text-teal-400 mb-1.5 flex items-center gap-2">
                🔒 Sécurité
              </h3>
              <p className="text-sm text-zinc-400">
                Un environnement fermé, chiffré et contrôlé.
              </p>
            </div>
          </div>
        </div>
      </div>
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-end">
          <Appearance />
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">{children}</div>
        </div>
        <Footer />
      </div>
    </div>
  )
}
