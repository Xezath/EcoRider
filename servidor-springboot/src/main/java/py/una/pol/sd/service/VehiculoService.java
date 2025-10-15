package py.una.pol.sd.service;
import java.util.ArrayList;
import java.util.List; 
import java.util.Optional; 
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import py.una.pol.sd.model.Vehiculo;
import py.una.pol.sd.repository.VehiculoRepository;


@Service
public class VehiculoService {

    @Autowired
    private VehiculoRepository repo;

    public List<Vehiculo> listar() {
        return repo.findAll();
    }

    public Vehiculo guardar(Vehiculo v) {
        return repo.save(v);
    }

    public Optional<Vehiculo> buscarPorId(Long id) {
        return repo.findById(id);
    }

    public void eliminar(Long id) {
        repo.deleteById(id);
    }

    
}
