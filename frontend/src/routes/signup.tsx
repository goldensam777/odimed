import { zodResolver } from "@hookform/resolvers/zod"
import {
  createFileRoute,
  Link as RouterLink,
  redirect,
} from "@tanstack/react-router"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { AuthLayout } from "@/components/Common/AuthLayout"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import { PasswordInput } from "@/components/ui/password-input"
import useAuth, { isLoggedIn } from "@/hooks/useAuth"

const formSchema = z
  .object({
    email: z.email(),
    full_name: z.string().min(1, { message: "Le nom complet est requis" }),
    password: z
      .string()
      .min(1, { message: "Le mot de passe est requis" })
      .min(8, { message: "Le mot de passe doit faire au moins 8 caractères" }),
    confirm_password: z
      .string()
      .min(1, { message: "La confirmation est requise" }),
    type_utilisateur: z.enum(["medecin", "patient", "pharmacien"], {
      required_error: "Veuillez sélectionner un type de profil",
    }),
    numero_ordre: z.string().optional(),
    specialite: z.string().optional(),
    pays_exercice: z.string().optional(),
    numero_licence: z.string().optional(),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Les mots de passe ne correspondent pas",
    path: ["confirm_password"],
  })

type FormData = z.infer<typeof formSchema>

export const Route = createFileRoute("/signup")({
  component: SignUp,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Sign Up - Odimed",
      },
    ],
  }),
})

function SignUp() {
  const { signUpMutation } = useAuth()
  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      email: "",
      full_name: "",
      password: "",
      confirm_password: "",
      type_utilisateur: "medecin",
      numero_ordre: "",
      specialite: "",
      pays_exercice: "",
      numero_licence: "",
    },
  })

  const selectedRole = form.watch("type_utilisateur")

  const onSubmit = (data: FormData) => {
    if (signUpMutation.isPending) return

    // exclude confirm_password from submission data
    const { confirm_password: _confirm_password, ...submitData } = data
    // cast to any to bypass strict typing before openapi-ts sync
    signUpMutation.mutate(submitData as any)
  }

  return (
    <AuthLayout>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-6"
        >
          <div className="flex flex-col items-center gap-2 text-center">
            <h1 className="text-2xl font-bold">Créer un compte</h1>
          </div>

          <div className="grid gap-4">
            
            <FormField
              control={form.control}
              name="type_utilisateur"
              render={({ field }) => (
                <FormItem className="space-y-3">
                  <FormLabel>Je suis un...</FormLabel>
                  <FormControl>
                    <div className="grid grid-cols-3 gap-2">
                      {[
                        { id: "medecin", label: "Médecin" },
                        { id: "patient", label: "Patient" },
                        { id: "pharmacien", label: "Pharmacien" },
                      ].map((role) => (
                        <label
                          key={role.id}
                          className={`flex cursor-pointer items-center justify-center rounded-md border-2 p-3 text-sm font-medium transition-colors hover:bg-muted ${
                            field.value === role.id
                              ? "border-primary text-primary"
                              : "border-muted text-muted-foreground"
                          }`}
                        >
                          <input
                            type="radio"
                            className="sr-only"
                            {...field}
                            value={role.id}
                            checked={field.value === role.id}
                          />
                          {role.label}
                        </label>
                      ))}
                    </div>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="full_name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Nom Complet</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="full-name-input"
                      placeholder="Dr. Jean Dupont"
                      type="text"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      data-testid="email-input"
                      placeholder="jean.dupont@example.com"
                      type="email"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            {/* Conditional Fields for Médecin */}
            {selectedRole === "medecin" && (
              <div className="grid grid-cols-2 gap-4 bg-muted/30 p-4 rounded-xl border border-border">
                <FormField
                  control={form.control}
                  name="numero_ordre"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Numéro d'Ordre</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: 12345678" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="specialite"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Spécialité</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: Cardiologie" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="pays_exercice"
                  render={({ field }) => (
                    <FormItem className="col-span-2">
                      <FormLabel>Pays d'Exercice</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: France" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}
            
            {/* Conditional Fields for Pharmacien */}
            {selectedRole === "pharmacien" && (
              <div className="bg-muted/30 p-4 rounded-xl border border-border">
                <FormField
                  control={form.control}
                  name="numero_licence"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Numéro de Licence</FormLabel>
                      <FormControl>
                        <Input placeholder="Ex: PHARM-98765" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            )}

            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Mot de passe</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="password-input"
                      placeholder="Mot de passe"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirm_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Confirmer le mot de passe</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="confirm-password-input"
                      placeholder="Confirmer"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <LoadingButton
              type="submit"
              className="w-full"
              loading={signUpMutation.isPending}
            >
              S'inscrire
            </LoadingButton>
          </div>

          <div className="text-center text-sm">
            Déjà un compte ?{" "}
            <RouterLink to="/login" className="underline underline-offset-4">
              Se connecter
            </RouterLink>
          </div>
        </form>
      </Form>
    </AuthLayout>
  )
}
