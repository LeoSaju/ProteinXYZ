# myapp/views.py

from django.shortcuts import render
from .forms import UploadPDBFileForm
from Bio.PDB import PDBParser
import os

def get_protein_size(pdb_file_path):
    parser = PDBParser()
    structure = parser.get_structure('protein', pdb_file_path)
    
    min_x = min_y = min_z = float('inf')
    max_x = max_y = max_z = float('-inf')
    
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    coord = atom.coord
                    x, y, z = coord
                    if x < min_x:
                        min_x = x
                    if y < min_y:
                        min_y = y
                    if z < min_z:
                        min_z = z
                    if x > max_x:
                        max_x = x
                    if y > max_y:
                        max_y = y
                    if z > max_z:
                        max_z = z
    
    size_x = max_x - min_x
    size_y = max_y - min_y
    size_z = max_z - min_z
    
    return size_x, size_y, size_z

def protein_view(request):
    form = UploadPDBFileForm()
    size_x = size_y = size_z = None

    if request.method == 'POST':
        form = UploadPDBFileForm(request.POST, request.FILES)
        if form.is_valid():
            pdb_file = request.FILES['pdb_file']
            file_path = os.path.join('uploads', pdb_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in pdb_file.chunks():
                    destination.write(chunk)
            
            size_x, size_y, size_z = get_protein_size(file_path)
    
    context = {
        'form': form,
        'size_x': size_x,
        'size_y': size_y,
        'size_z': size_z,
    }
    return render(request, 'protein.html', context)
