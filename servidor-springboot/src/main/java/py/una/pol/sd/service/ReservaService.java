package py.una.pol.sd.service;

import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import py.una.pol.sd.model.Reserva;
import py.una.pol.sd.repository.ReservaRepository;

@Service
public class ReservaService {

    @Autowired
    private ReservaRepository repo;

    public List<Reserva> listar() {
        return repo.findAll();
    }

    public Reserva guardar(Reserva r) {
        return repo.save(r);
    }

    public Optional<Reserva> buscarPorId(Long id) {
        return repo.findById(id);
    }

    public void eliminar(Long id) {
        repo.deleteById(id);
    }
}
