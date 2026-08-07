import { useEditor, EditorContent } from '@tiptap/react'
import StarterKit from '@tiptap/starter-kit'
import { Table } from '@tiptap/extension-table'
import { TableRow } from '@tiptap/extension-table-row'
import { TableCell } from '@tiptap/extension-table-cell'
import { TableHeader } from '@tiptap/extension-table-header'
import { Bold, Italic, Strikethrough, Heading1, Heading2, List, ListOrdered, Undo, Redo, Rows3, Columns3, Trash2, PlusCircle, MinusCircle } from 'lucide-react'
import { Button } from '@/components/ui/button'

interface PaperEditorProps {
  paperSize: 'A4' | 'A5'
  initialContent?: string
}

const tableHTML = `
  <table style="width: 100%;">
    <tbody>
      <tr>
        <th>Médicament</th>
        <th>Posologie</th>
      </tr>
      <tr>
        <td>Amoxicilline 1g</td>
        <td>1 comprimé matin et soir (6 jours)</td>
      </tr>
      <tr>
        <td>Doliprane 1000mg</td>
        <td>1 comprimé toutes les 6h si douleurs</td>
      </tr>
    </tbody>
  </table>
`

const MenuBar = ({ editor, paperSize }: { editor: any, paperSize: 'A4' | 'A5' }) => {
  if (!editor) {
    return null
  }

  // The toolbar width matches the paper width
  const toolbarWidth = paperSize === 'A4' ? 'max-w-[210mm]' : 'max-w-[148mm]'

  return (
    <div className={`flex flex-wrap items-center gap-1 p-1.5 bg-card border border-border shadow-md rounded-xl mx-auto sticky top-4 z-30 mb-4 overflow-x-auto text-foreground w-full ${toolbarWidth} shrink-0`}>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleBold().run()} disabled={!editor.can().chain().focus().toggleBold().run()} data-active={editor.isActive('bold') ? 'true' : 'false'}>
        <Bold className={`h-4 w-4 ${editor.isActive('bold') ? 'text-primary' : ''}`} />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleItalic().run()} disabled={!editor.can().chain().focus().toggleItalic().run()} data-active={editor.isActive('italic') ? 'true' : 'false'}>
        <Italic className={`h-4 w-4 ${editor.isActive('italic') ? 'text-primary' : ''}`} />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleStrike().run()} disabled={!editor.can().chain().focus().toggleStrike().run()} data-active={editor.isActive('strike') ? 'true' : 'false'}>
        <Strikethrough className={`h-4 w-4 ${editor.isActive('strike') ? 'text-primary' : ''}`} />
      </Button>
      
      <div className="w-px h-6 bg-border mx-1 shrink-0" />
      
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} data-active={editor.isActive('heading', { level: 1 }) ? 'true' : 'false'}>
        <Heading1 className={`h-4 w-4 ${editor.isActive('heading', { level: 1 }) ? 'text-primary' : ''}`} />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} data-active={editor.isActive('heading', { level: 2 }) ? 'true' : 'false'}>
        <Heading2 className={`h-4 w-4 ${editor.isActive('heading', { level: 2 }) ? 'text-primary' : ''}`} />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().toggleBulletList().run()} data-active={editor.isActive('bulletList') ? 'true' : 'false'}>
        <List className={`h-4 w-4 ${editor.isActive('bulletList') ? 'text-primary' : ''}`} />
      </Button>

      {/* Contextual Table Tools (only show when cursor is inside a table) */}
      {editor.isActive('table') && (
        <>
          <div className="w-px h-6 bg-border mx-1 shrink-0" />
          <div className="flex items-center gap-1 bg-primary/10 p-0.5 rounded border border-primary/20 shrink-0">
            <Button variant="ghost" size="sm" className="h-7 px-2 text-xs gap-1 text-primary hover:bg-primary/20" onClick={() => editor.chain().focus().addRowAfter().run()}>
              <PlusCircle className="h-3 w-3" /> Ligne
            </Button>
            <Button variant="ghost" size="sm" className="h-7 px-2 text-xs gap-1 text-destructive hover:bg-destructive/10 hover:text-destructive" onClick={() => editor.chain().focus().deleteRow().run()}>
              <MinusCircle className="h-3 w-3" /> Ligne
            </Button>
            <div className="w-px h-4 bg-primary/20 mx-1 shrink-0" />
            <Button variant="ghost" size="sm" className="h-7 px-2 text-xs gap-1 text-primary hover:bg-primary/20" onClick={() => editor.chain().focus().addColumnAfter().run()}>
              <PlusCircle className="h-3 w-3" /> Colonne
            </Button>
            <Button variant="ghost" size="sm" className="h-7 px-2 text-xs gap-1 text-destructive hover:bg-destructive/10 hover:text-destructive" onClick={() => editor.chain().focus().deleteColumn().run()}>
              <MinusCircle className="h-3 w-3" /> Colonne
            </Button>
          </div>
        </>
      )}

      <div className="flex-1 min-w-[20px]" />
      
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().undo().run()} disabled={!editor.can().chain().focus().undo().run()}>
        <Undo className="h-4 w-4" />
      </Button>
      <Button variant="ghost" size="icon" className="h-8 w-8 hover:bg-muted shrink-0" onClick={() => editor.chain().focus().redo().run()} disabled={!editor.can().chain().focus().redo().run()}>
        <Redo className="h-4 w-4" />
      </Button>
    </div>
  )
}

export function PaperEditor({ paperSize, initialContent }: PaperEditorProps) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Table.configure({
        resizable: true,
      }),
      TableRow,
      TableCell,
      TableHeader,
    ],
    content: initialContent || `
      <h2>Dr. Jean Dupont</h2>
      <p>Cardiologue - N° Ordre: 123456789</p>
      <hr />
      <p><strong>Patient :</strong> _________________</p>
      <p><strong>Date :</strong> ${new Date().toLocaleDateString('fr-FR')}</p>
      <br />
      ${tableHTML}
      <br />
      <p><em>Notes complémentaires :</em></p>
      <p></p>
      <br /><br /><br />
      <p style="text-align: right;">[Signature ici]</p>
    `,
    editorProps: {
      attributes: {
        class: 'prose prose-sm sm:prose lg:prose-lg xl:prose-2xl mx-auto focus:outline-none min-h-full',
      },
    },
  })

  // Reverted to responsive widths to avoid the cutoff issue on mobile
  const paperStyles = {
    'A4': 'w-full max-w-[210mm] min-h-[100vh] sm:min-h-[297mm]',
    'A5': 'w-full max-w-[148mm] min-h-[100vh] sm:min-h-[210mm]',
  }

  return (
    <div className="flex flex-col items-center w-full pb-12 pt-2">
      <div className="w-full px-4 md:px-0 flex flex-col items-center">
        <MenuBar editor={editor} paperSize={paperSize} />
        
        <div className={`relative bg-white shadow-xl ${paperStyles[paperSize]} transition-all duration-300 ease-in-out text-slate-900 border border-slate-200 flex flex-col shrink-0`}>
        {/* 
          TipTap Table styling requires some raw CSS because Tailwind prose doesn't 
          handle the complex table borders and resize handles of TipTap perfectly out of the box.
        */}
        <style>{`
          .ProseMirror {
            color: #0f172a !important; /* Force dark text regardless of dark mode */
          }
          .ProseMirror p, .ProseMirror h1, .ProseMirror h2, .ProseMirror h3, .ProseMirror strong, .ProseMirror em {
            color: inherit !important;
          }
          .ProseMirror table {
            border-collapse: collapse;
            table-layout: fixed;
            width: 100%;
            margin: 0;
            overflow: hidden;
          }
          .ProseMirror td,
          .ProseMirror th {
            min-width: 1em;
            border: 1px solid #ced4da;
            padding: 8px;
            vertical-align: top;
            box-sizing: border-box;
            position: relative;
          }
          .ProseMirror th {
            font-weight: bold;
            text-align: left;
            background-color: #f1f3f5;
          }
          .ProseMirror .selectedCell:after {
            z-index: 2;
            position: absolute;
            content: "";
            left: 0; right: 0; top: 0; bottom: 0;
            background: rgba(200, 200, 255, 0.4);
            pointer-events: none;
          }
          .ProseMirror .column-resize-handle {
            position: absolute;
            right: -2px;
            top: 0;
            bottom: -2px;
            width: 4px;
            background-color: #adf;
            pointer-events: none;
          }
        `}</style>
        
        <div className="p-4 md:p-12 h-full">
          <EditorContent editor={editor} className="h-full" />
        </div>
      </div>
    </div>
    </div>
  )
}
