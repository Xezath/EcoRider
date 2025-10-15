package py.una.pol.sd.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import py.una.pol.sd.model.Viaje;
import py.una.pol.sd.repository.ViajeRepository;

@Service
public class ViajeService {
    @Autowired
    private ViajeRepository repository;

    public Viaje guardar(Viaje v) {
        return repository.save(v);
    }

    public List<Viaje> listar() {
        return (List<Viaje>) repository.findAll();
    }

    public Viaje obtenerPorId(Long id) {
        return repository.findById(id).orElse(null);
    }

    public void eliminar(Long id) {
        repository.deleteById(id);
    }
        
    public Optional<Viaje> buscarPorId(Long id) {
        return repository.findById(id);
    }

}
